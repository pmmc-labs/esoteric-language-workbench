// Tokens to an AST of plain objects with a `kind` and a `pos` (D29). Step 2
// parses expressions on ints, bools and nil, names and calls, and the
// statements `let`, assignment, `if`, `while`, `for`, `break` and `continue`;
// each later step adds members to Expr and Stmt and cases to the functions
// below.
import { compileError } from './errors.ts';
import type { Pos } from './errors.ts';
import type { Token } from './lexer.ts';

export type BinaryOp = '+' | '-' | '*' | '/' | '%' | '==' | '!=' | '<' | '<=' | '>' | '>=';

// `pos` of a unary or binary node is its operator: where faults point.
export type Expr =
  | { kind: 'int'; pos: Pos; value: bigint }
  | { kind: 'bool'; pos: Pos; value: boolean }
  | { kind: 'nil'; pos: Pos }
  // `cname` is filled in by the resolver: the C variable's name.
  | { kind: 'name'; pos: Pos; name: string; cname?: string }
  | { kind: 'unary'; pos: Pos; op: '-' | 'not'; operand: Expr }
  | { kind: 'binary'; pos: Pos; op: BinaryOp; left: Expr; right: Expr }
  // `and`/`or` short-circuit, so they are not `binary`.
  | { kind: 'logic'; pos: Pos; op: 'and' | 'or'; left: Expr; right: Expr }
  // `target` is filled in by the resolver: 'builtin' or (step 3) 'fn'.
  | { kind: 'call'; pos: Pos; name: string; args: Expr[]; target?: 'builtin' | 'fn' };

export type AssignOp = '=' | '+=' | '-=' | '*=' | '/=' | '%=';

// What follows a variable in an assignment target: `[index]` or `.name`
// (steps 5 and 6). Empty until then, but the shape is here so that a path
// is a variable and a list of steps.
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
  | { kind: 'continue'; pos: Pos };

export type Iter =
  | { kind: 'range'; lo: Expr; loPos: Pos; hi: Expr; hiPos: Pos; inclusive: boolean }
  | { kind: 'each'; expr: Expr; exprPos: Pos };

export type Program = { kind: 'program'; body: Stmt[] };

export function parse(tokens: Token[]): Program {
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
  // comparisons, + -, * / %, prefix -, then calls and atoms. `else` (step 7)
  // goes between * and prefix -, and `in` joins the comparisons.
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
  const isComparison = (t: Token) => t.kind === 'op' && COMPARISONS.includes(t.text);

  function comparison(): Expr {
    const left = additive();
    if (!isComparison(peek())) return left;
    const op = operator();
    const right = additive();
    if (isComparison(peek())) throw compileError(peek().pos, 'comparisons do not chain');
    return { kind: 'binary', pos: op.pos, op: op.text as BinaryOp, left, right };
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
    if (!isOp(t, '-')) return primary();
    next();
    return { kind: 'unary', pos: t.pos, op: '-', operand: unary() };
  }

  function primary(): Expr {
    const t = peek();
    if (t.kind === 'int') { next(); return { kind: 'int', pos: t.pos, value: t.value }; }
    if (isKw(t, 'true') || isKw(t, 'false')) {
      next();
      return { kind: 'bool', pos: t.pos, value: t.text === 'true' };
    }
    if (isKw(t, 'nil')) { next(); return { kind: 'nil', pos: t.pos }; }
    if (isOp(t, '(')) {
      next();
      const inner = expr();
      expect(')');
      return inner;
    }
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
    t.kind === 'int' || t.kind === 'name' || isOp(t, '(') || isOp(t, '-') ||
    isKw(t, 'true') || isKw(t, 'false') || isKw(t, 'nil') || isKw(t, 'not');

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

  function statement(): Stmt {
    const t = peek();
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
      // The target is a variable and its steps (paths arrive in step 5).
      if (e.kind !== 'name') throw compileError(t.pos, 'cannot assign to this');
      const op = operator();
      const target: Target = { kind: 'target', pos: t.pos, name: e.name, steps: [] };
      return { kind: 'assign', pos: op.pos, op: op.text as AssignOp, target, value: expr() };
    }
    return { kind: 'exprStmt', pos: t.pos, expr: e };
  }

  const body: Stmt[] = [];
  for (;;) {
    while (isSeparator(peek())) next();
    if (peek().kind === 'eof') break;
    body.push(statement());
    // A statement ends at a newline, a `;` or the end of the file.
    if (!isSeparator(peek()) && peek().kind !== 'eof') expected('newline');
  }
  return { kind: 'program', body };
}
