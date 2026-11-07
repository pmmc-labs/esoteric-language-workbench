// Tokens to an AST of plain objects with a `kind` and a `pos` (D29). Step 0
// parses calls of `print` with int arguments; each later step adds members to
// Expr and Stmt and cases to the functions below.
import { compileError } from './errors.ts';
import type { Pos } from './errors.ts';
import type { Token } from './lexer.ts';

export type Expr =
  | { kind: 'int'; pos: Pos; value: bigint }
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

  function expr(): Expr {
    const t = peek();
    if (t.kind === 'int') { next(); return { kind: 'int', pos: t.pos, value: t.value }; }
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

  function statement(): Stmt {
    const t = peek();
    if (t.kind !== 'name') return expected('a statement');
    const e = call();
    return { kind: 'exprStmt', pos: t.pos, expr: e };
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
