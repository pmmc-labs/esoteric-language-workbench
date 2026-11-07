// Tokens to an AST of plain objects with a `kind` and a `pos` (D29). Step 1
// parses expressions on ints, bools and nil, and calls of `print`; each later
// step adds members to Expr and Stmt and cases to the functions below.
import { compileError } from './errors.ts';
import type { Pos } from './errors.ts';
import type { Token } from './lexer.ts';

export type BinaryOp = '+' | '-' | '*' | '/' | '%' | '==' | '!=' | '<' | '<=' | '>' | '>=';

// `pos` of a unary or binary node is its operator: where faults point.
export type Expr =
  | { kind: 'int'; pos: Pos; value: bigint }
  | { kind: 'bool'; pos: Pos; value: boolean }
  | { kind: 'nil'; pos: Pos }
  | { kind: 'unary'; pos: Pos; op: '-' | 'not'; operand: Expr }
  | { kind: 'binary'; pos: Pos; op: BinaryOp; left: Expr; right: Expr }
  // `and`/`or` short-circuit, so they are not `binary`.
  | { kind: 'logic'; pos: Pos; op: 'and' | 'or'; left: Expr; right: Expr }
  // `target` is filled in by the resolver: 'builtin' or (step 3) 'fn'.
  | { kind: 'call'; pos: Pos; name: string; args: Expr[]; target?: 'builtin' | 'fn' };

export type Stmt = { kind: 'exprStmt'; pos: Pos; expr: Expr };

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
    // Until variables arrive (step 2) a name can only start a call.
    if (t.kind === 'name') return call();
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

  function statement(): Stmt {
    const t = peek();
    if (!startsExpression(t)) return expected('a statement');
    // Whether it is a call is the resolver's business: `42` parses, then is
    // `expression statement must be a call`.
    return { kind: 'exprStmt', pos: t.pos, expr: expr() };
  }

  const isSeparator = (t: Token) => t.kind === 'newline' || isOp(t, ';');
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
