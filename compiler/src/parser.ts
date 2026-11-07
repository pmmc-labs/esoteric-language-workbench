import { fail } from "./errors.ts";
import type { Token } from "./lexer.ts";

export type Expr = { k: "int"; v: string; line: number; col: number };
export type Stmt = { k: "print"; e: Expr; line: number; col: number };
export type Program = { k: "program"; stmts: Stmt[] };

// What a token is called in "expected THING, found TOKEN" (D33).
const describe = (t: Token) => (t.k === "eof" ? "end of file" : `'${t.text}'`);

export function parse(toks: Token[]): Program {
  let p = 0;
  const stmts: Stmt[] = [];
  while (toks[p].k !== "eof") {
    const t = toks[p];
    if (t.k !== "kw" || t.text !== "print") fail(t.line, t.col, `expected statement, found ${describe(t)}`);
    p++;
    const n = toks[p];
    if (n.k !== "int") fail(n.line, n.col, `expected expression, found ${describe(n)}`);
    p++;
    stmts.push({ k: "print", e: { k: "int", v: n.val, line: n.line, col: n.col }, line: t.line, col: t.col });
  }
  return { k: "program", stmts };
}
