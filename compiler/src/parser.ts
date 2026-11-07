// Tokens to an AST of plain objects with a `kind` and a `pos` (D29). Step 6
// parses expressions on ints, bools, nil, strings, lists and maps, names,
// calls, indexing and fields, and the statements `fn`, `return`, `let`,
// assignment to a path of index and field steps, `if`, `while`, `for`,
// `break` and `continue`; each later step adds members to Expr and Stmt and
// cases to the functions below.
import { compileError } from './errors.ts';
import type { Pos } from './errors.ts';
import type { StringPart, Token } from './lexer.ts';

export type BinaryOp =
  | '+' | '-' | '*' | '/' | '%' | '==' | '!=' | '<' | '<=' | '>' | '>=' | 'in' | 'not in';

// `pos` of a unary or binary node is its operator: where faults point (for
// `not in`, the `not`). An index's is its `[`, a field's its `.`; a string's
// its opening quote.
export type Expr =
  | { kind: 'int'; pos: Pos; value: bigint }
  | { kind: 'bool'; pos: Pos; value: boolean }
  | { kind: 'nil'; pos: Pos }
  // Text and interpolated expressions in source order; an interpolation's pos
  // is its `{`.
  | { kind: 'string'; pos: Pos; parts: StringPartNode[] }
  | { kind: 'index'; pos: Pos; target: Expr; index: Expr }
  // `pos` is the `[`.
  | { kind: 'list'; pos: Pos; items: Expr[] }
  // `pos` is the `{`. A key is a literal node, a string (a name is the string
  // it spells) or an int (a leading `-` folded in), at the key's first token.
  | { kind: 'map'; pos: Pos; entries: MapEntry[] }
  | { kind: 'field'; pos: Pos; target: Expr; name: string }
  // `cname` is filled in by the resolver: the C variable's name.
  | { kind: 'name'; pos: Pos; name: string; cname?: string }
  | { kind: 'unary'; pos: Pos; op: '-' | 'not'; operand: Expr }
  | { kind: 'binary'; pos: Pos; op: BinaryOp; left: Expr; right: Expr }
  // `and`/`or` short-circuit, so they are not `binary`.
  | { kind: 'logic'; pos: Pos; op: 'and' | 'or'; left: Expr; right: Expr }
  // `target` is filled in by the resolver: 'builtin' or 'fn' (a user function).
  | { kind: 'call'; pos: Pos; name: string; args: Expr[]; target?: 'builtin' | 'fn' };

export type MapEntry = { key: Expr; value: Expr };

export type StringPartNode =
  | { kind: 'text'; value: string }
  | { kind: 'interp'; pos: Pos; expr: Expr };

export type AssignOp = '=' | '+=' | '-=' | '*=' | '/=' | '%=';

// What follows a variable in an assignment target: `[index]` or `.name`.
// `pos` is the `[` (or the `.`), where a fault in that step points. A path is
// a variable and a list of steps.
export type Step =
  | { kind: 'index'; pos: Pos; index: Expr }
  | { kind: 'field'; pos: Pos; name: string };

export type Target = { kind: 'target'; pos: Pos; name: string; steps: Step[]; cname?: string };

// Each statement's `pos` is its first token, except an assignment's, which is
// its operator (where a compound assignment's faults point). `condPos`,
// `loPos` and the like are the first token of an expression: where its
// faults point.
export type Stmt =
  | { kind: 'exprStmt'; pos: Pos; expr: Expr }
  | { kind: 'let'; pos: Pos; name: string; namePos: Pos; value: Expr; cname?: string }
  | { kind: 'assign'; pos: Pos; op: AssignOp; target: Target; value: Expr }
  // `else` is null, a block, or (for `else if`) a block of the one `if`.
  | { kind: 'if'; pos: Pos; cond: Expr; condPos: Pos; then: Stmt[]; else: Stmt[] | null }
  | { kind: 'while'; pos: Pos; cond: Expr; condPos: Pos; body: Stmt[] }
  | { kind: 'for'; pos: Pos; name: string; namePos: Pos; iter: Iter; body: Stmt[]; cname?: string }
  | { kind: 'break'; pos: Pos }
  | { kind: 'continue'; pos: Pos }
  // Top level only. `pos` is the keyword; `namePos` the name, where
  // `duplicate function` and `print is a builtin` point.
  | { kind: 'fn'; pos: Pos; name: string; namePos: Pos; params: Param[]; body: Stmt[] }
  // `value` is null for a bare `return`.
  | { kind: 'return'; pos: Pos; value: Expr | null };

export type Param = { name: string; pos: Pos; cname?: string };

export type Iter =
  | { kind: 'range'; lo: Expr; loPos: Pos; hi: Expr; hiPos: Pos; inclusive: boolean }
  | { kind: 'each'; expr: Expr; exprPos: Pos };

export type Program = { kind: 'program'; body: Stmt[] };

export function parse(input: Token[]): Program {
  // Swapped for an interpolation's own tokens while one is parsed.
  let tokens = input;
  let i = 0;
  const peek = () => tokens[i];
  const next = () => tokens[Math.min(i++, tokens.length - 1)];
  const isOp = (t: Token, text: string) => t.kind === 'op' && t.text === text;

  function describe(t: Token): string {
    if (t.kind === 'eof') return 'end of file';
    if (t.kind === 'newline') return 'newline';
    if (t.kind === 'string') return 'string';
    return `'${t.text}'`;
  }
  function expected(what: string): never {
    const t = peek();
    throw compileError(t.pos, `expected ${what}, found ${describe(t)}`);
  }
  function expect(text: string): Token {
    if (!isOp(peek(), text)) expected(`'${text}'`);
    return next();
  }

  const isKw = (t: Token, text: string) => t.kind === 'kw' && t.text === text;
  const skipNewlines = () => { while (peek().kind === 'newline') next(); };
  // A newline after a binary operator doesn't end the statement.
  function operator(): Token { const t = next(); skipNewlines(); return t; }

  // Precedence, loosest first (LANGUAGE.md, Expressions): or, and, not,
  // comparisons (`in` and `not in` among them), + -, * / %, prefix -, then
  // calls, indexes and atoms. `else` (step 7) goes between * and prefix -.
  function expr(): Expr { return orExpr(); }

  function orExpr(): Expr {
    let left = andExpr();
    while (isKw(peek(), 'or')) {
      const op = operator();
      left = { kind: 'logic', pos: op.pos, op: 'or', left, right: andExpr() };
    }
    return left;
  }

  function andExpr(): Expr {
    let left = notExpr();
    while (isKw(peek(), 'and')) {
      const op = operator();
      left = { kind: 'logic', pos: op.pos, op: 'and', left, right: notExpr() };
    }
    return left;
  }

  function notExpr(): Expr {
    const t = peek();
    if (!isKw(t, 'not')) return comparison();
    next();
    return { kind: 'unary', pos: t.pos, op: 'not', operand: notExpr() };
  }

  const COMPARISONS = ['==', '!=', '<', '<=', '>', '>='];
  const isNotIn = () => isKw(peek(), 'not') && isKw(tokens[i + 1], 'in');
  const isComparison = () =>
    (peek().kind === 'op' && COMPARISONS.includes(peek().text)) || isKw(peek(), 'in') || isNotIn();

  function comparison(): Expr {
    const left = additive();
    if (!isComparison()) return left;
    // `not in` is one operator, whose position is the `not`.
    const notIn = isNotIn();
    const op = operator();
    if (notIn) next();
    skipNewlines();
    const right = additive();
    if (isComparison()) throw compileError(peek().pos, 'comparisons do not chain');
    return { kind: 'binary', pos: op.pos, op: notIn ? 'not in' : (op.text as BinaryOp), left, right };
  }

  function additive(): Expr {
    let left = multiplicative();
    while (isOp(peek(), '+') || isOp(peek(), '-')) {
      const op = operator();
      left = { kind: 'binary', pos: op.pos, op: op.text as BinaryOp, left, right: multiplicative() };
    }
    return left;
  }

  function multiplicative(): Expr {
    let left = unary();
    while (isOp(peek(), '*') || isOp(peek(), '/') || isOp(peek(), '%')) {
      const op = operator();
      left = { kind: 'binary', pos: op.pos, op: op.text as BinaryOp, left, right: unary() };
    }
    return left;
  }

  function unary(): Expr {
    const t = peek();
    if (!isOp(t, '-')) return postfix();
    next();
    return { kind: 'unary', pos: t.pos, op: '-', operand: unary() };
  }

  // Indexes and fields bind tighter than prefix minus: `-s[0]` is `-(s[0])`.
  // The lexer drops newlines inside `[ ]`. A `.` must be on the line of what
  // it follows, since a newline ends the statement.
  function postfix(): Expr {
    let e = primary();
    for (;;) {
      if (isOp(peek(), '[')) {
        const bracket = next();
        const index = expr();
        expect(']');
        e = { kind: 'index', pos: bracket.pos, target: e, index };
      } else if (isOp(peek(), '.')) {
        const dot = next();
        const name = peek();
        if (name.kind !== 'name') return expected('a name');
        next();
        e = { kind: 'field', pos: dot.pos, target: e, name: name.text };
      } else {
        return e;
      }
    }
  }

  // A key is a name (the string it spells), a string without interpolation,
  // or an int literal with an optional `-`; judged by its first token(s).
  function mapKey(): Expr {
    const t = peek();
    if (t.kind === 'name') {
      next();
      return { kind: 'string', pos: t.pos, parts: [{ kind: 'text', value: t.text }] };
    }
    if (t.kind === 'string' && t.parts.every((p) => p.kind === 'text')) {
      next();
      return { kind: 'string', pos: t.pos, parts: t.parts.map((p): StringPartNode => p as StringPartNode) };
    }
    if (t.kind === 'int') { next(); return { kind: 'int', pos: t.pos, value: t.value }; }
    const after = tokens[i + 1];
    if (isOp(t, '-') && after.kind === 'int') {
      next();
      next();
      return { kind: 'int', pos: t.pos, value: -after.value };
    }
    throw compileError(t.pos, 'map key must be a name, a string or an int');
  }

  // Newlines are ignored anywhere inside the braces (LANGUAGE.md, Lexical).
  function mapLiteral(): Expr {
    const open = next();
    const entries: MapEntry[] = [];
    skipNewlines();
    while (!isOp(peek(), '}')) {
      const key = mapKey();
      skipNewlines();
      expect(':');
      skipNewlines();
      const value = expr();
      entries.push({ key, value });
      skipNewlines();
      if (!isOp(peek(), ',')) break;
      next();
      skipNewlines();
    }
    expect('}');
    return { kind: 'map', pos: open.pos, entries };
  }

  // The tokens of one `{expr}` are parsed on their own, closed by a `}` at
  // the position the lexer saw it.
  function interpolation(part: Extract<StringPart, { kind: 'interp' }>): Expr {
    const saved = { tokens, i };
    tokens = [...part.tokens, { kind: 'op', text: '}', pos: part.end }];
    i = 0;
    const e = expr();
    expect('}');
    tokens = saved.tokens;
    i = saved.i;
    return e;
  }

  function primary(): Expr {
    const t = peek();
    if (t.kind === 'int') { next(); return { kind: 'int', pos: t.pos, value: t.value }; }
    if (isKw(t, 'true') || isKw(t, 'false')) {
      next();
      return { kind: 'bool', pos: t.pos, value: t.text === 'true' };
    }
    if (isKw(t, 'nil')) { next(); return { kind: 'nil', pos: t.pos }; }
    if (t.kind === 'string') {
      next();
      const parts = t.parts.map((p): StringPartNode =>
        p.kind === 'text' ? p : { kind: 'interp', pos: p.pos, expr: interpolation(p) });
      return { kind: 'string', pos: t.pos, parts };
    }
    if (isOp(t, '(')) {
      next();
      const inner = expr();
      expect(')');
      return inner;
    }
    if (isOp(t, '[')) {
      // Items may end with a comma, like an argument list (LANGUAGE.md,
      // Literals); the lexer drops the newlines inside the brackets.
      next();
      const items: Expr[] = [];
      while (!isOp(peek(), ']')) {
        items.push(expr());
        if (!isOp(peek(), ',')) break;
        next();
      }
      expect(']');
      return { kind: 'list', pos: t.pos, items };
    }
    if (isOp(t, '{')) return mapLiteral();
    if (t.kind === 'name') {
      if (isOp(tokens[i + 1], '(')) return call();
      next();
      return { kind: 'name', pos: t.pos, name: t.text };
    }
    return expected('an expression');
  }

  function call(): Expr {
    const name = next(); // a name
    expect('(');
    const args: Expr[] = [];
    while (!isOp(peek(), ')')) {
      args.push(expr());
      if (!isOp(peek(), ',')) break;
      next();
    }
    expect(')');
    return { kind: 'call', pos: name.pos, name: name.text, args };
  }

  const startsExpression = (t: Token) =>
    t.kind === 'int' || t.kind === 'string' || t.kind === 'name' || isOp(t, '(') || isOp(t, '[') || isOp(t, '-') ||
    isKw(t, 'true') || isKw(t, 'false') || isKw(t, 'nil') || isKw(t, 'not');

  // The target of an assignment is a name and any number of steps, which is
  // an expression of names, indexes and fields: anything else cannot be
  // assigned to.
  function targetOf(e: Expr, pos: Pos): Target | null {
    const steps: Step[] = [];
    let r = e;
    while (r.kind === 'index' || r.kind === 'field') {
      steps.unshift(r.kind === 'index'
        ? { kind: 'index', pos: r.pos, index: r.index }
        : { kind: 'field', pos: r.pos, name: r.name });
      r = r.target;
    }
    if (r.kind !== 'name') return null;
    return { kind: 'target', pos, name: r.name, steps };
  }

  const isSeparator = (t: Token) => t.kind === 'newline' || isOp(t, ';');
  const ASSIGN_OPS = ['=', '+=', '-=', '*=', '/=', '%='];

  // `{ statements }`: statements are separated by newlines or `;`, and a `}`
  // ends the last one.
  function block(): Stmt[] {
    expect('{');
    const stmts: Stmt[] = [];
    for (;;) {
      while (isSeparator(peek())) next();
      if (isOp(peek(), '}')) { next(); return stmts; }
      if (peek().kind === 'eof') return expected("'}'");
      stmts.push(statement());
      if (!isSeparator(peek()) && !isOp(peek(), '}')) {
        if (peek().kind === 'eof') return expected("'}'");
        expected('newline');
      }
    }
  }

  function ifStmt(): Stmt {
    const kw = next();
    const condPos = peek().pos;
    const cond = expr();
    const then = block();
    let orElse: Stmt[] | null = null;
    // `else` may be on the line after the `}`.
    if (peek().kind === 'newline' && isKw(tokens[i + 1], 'else')) next();
    if (isKw(peek(), 'else')) {
      next();
      orElse = isKw(peek(), 'if') ? [ifStmt()] : block();
    }
    return { kind: 'if', pos: kw.pos, cond, condPos, then, else: orElse };
  }

  function forStmt(): Stmt {
    const kw = next();
    const nameTok = peek();
    if (nameTok.kind !== 'name') return expected('a name');
    next();
    if (!isKw(peek(), 'in')) return expected("'in'");
    next();
    const firstPos = peek().pos;
    const first = expr();
    let iter: Iter;
    if (isOp(peek(), '..') || isOp(peek(), '..=')) {
      const inclusive = next().text === '..=';
      const hiPos = peek().pos;
      iter = { kind: 'range', lo: first, loPos: firstPos, hi: expr(), hiPos, inclusive };
    } else {
      iter = { kind: 'each', expr: first, exprPos: firstPos };
    }
    return { kind: 'for', pos: kw.pos, name: nameTok.text, namePos: nameTok.pos, iter, body: block() };
  }

  // A parameter list is like an argument list: it may break across lines and
  // end with a comma (D34). The body's `{` must be on the line of the `)`.
  function fnStmt(): Stmt {
    const kw = next();
    const nameTok = peek();
    if (nameTok.kind !== 'name') return expected('a name');
    next();
    expect('(');
    const params: Param[] = [];
    while (!isOp(peek(), ')')) {
      const p = peek();
      if (p.kind !== 'name') return expected('a name');
      next();
      params.push({ name: p.text, pos: p.pos });
      if (!isOp(peek(), ',')) break;
      next();
    }
    expect(')');
    return { kind: 'fn', pos: kw.pos, name: nameTok.text, namePos: nameTok.pos, params, body: block() };
  }

  // `top` is true only for the program's own statements: a function is
  // defined there and nowhere else, which the parser knows at once.
  function statement(top = false): Stmt {
    const t = peek();
    if (isKw(t, 'fn')) {
      if (!top) throw compileError(t.pos, 'functions are defined at the top level');
      return fnStmt();
    }
    if (isKw(t, 'return')) {
      next();
      const n = peek();
      // A bare `return` ends at the end of its statement.
      if (isSeparator(n) || isOp(n, '}') || n.kind === 'eof') return { kind: 'return', pos: t.pos, value: null };
      return { kind: 'return', pos: t.pos, value: expr() };
    }
    if (isKw(t, 'let')) {
      next();
      const nameTok = peek();
      if (nameTok.kind !== 'name') return expected('a name');
      next();
      expect('=');
      skipNewlines();
      return { kind: 'let', pos: t.pos, name: nameTok.text, namePos: nameTok.pos, value: expr() };
    }
    if (isKw(t, 'if')) return ifStmt();
    if (isKw(t, 'while')) {
      next();
      const condPos = peek().pos;
      const cond = expr();
      return { kind: 'while', pos: t.pos, cond, condPos, body: block() };
    }
    if (isKw(t, 'for')) return forStmt();
    if (isKw(t, 'break')) { next(); return { kind: 'break', pos: t.pos }; }
    if (isKw(t, 'continue')) { next(); return { kind: 'continue', pos: t.pos }; }
    if (!startsExpression(t)) return expected('a statement');
    // An expression, then either the end of the statement or an assignment
    // operator. Whether an expression statement is a call is the resolver's
    // business: `42` parses, then is `expression statement must be a call`.
    const e = expr();
    if (peek().kind === 'op' && ASSIGN_OPS.includes(peek().text)) {
      const target = targetOf(e, t.pos);
      if (target === null) throw compileError(t.pos, 'cannot assign to this');
      const op = operator();
      return { kind: 'assign', pos: op.pos, op: op.text as AssignOp, target, value: expr() };
    }
    return { kind: 'exprStmt', pos: t.pos, expr: e };
  }

  const body: Stmt[] = [];
  for (;;) {
    while (isSeparator(peek())) next();
    if (peek().kind === 'eof') break;
    body.push(statement(true));
    // A statement ends at a newline, a `;` or the end of the file.
    if (!isSeparator(peek()) && peek().kind !== 'eof') expected('newline');
  }
  return { kind: 'program', body };
}
