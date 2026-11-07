import { fail } from "./errors.ts";
import type { Token } from "./lexer.ts";

// line, col is where a fault in the operation is reported (D23): the
// operator token for operators.
export type Expr =
  | { k: "int"; v: string; line: number; col: number }
  | { k: "bin"; op: string; l: Expr; r: Expr; line: number; col: number }
  | { k: "un"; op: string; e: Expr; line: number; col: number };
export type Stmt = { k: "print" | "write"; e: Expr; line: number; col: number };
export type Program = { k: "program"; stmts: Stmt[] };

// What a token is called in "expected THING, found TOKEN" (D33).
const describe = (t: Token) => (t.k === "eof" ? "end of file" : `'${t.text}'`);

const COMPARE = new Set(["=", "!=", "<", "<=", ">", ">="]);

// Precedence, loosest to tightest (LANGUAGE.md, Expressions): or, and,
// not, one comparison, + -, * / %, prefix -. Each level is a function.
export function parse(toks: Token[]): Program {
  let p = 0;
  const isOp = (t: Token, ...ops: string[]) => t.k === "op" && ops.includes(t.text);
  const isKw = (t: Token, w: string) => t.k === "kw" && t.text === w;

  const bin = (op: Token, l: Expr, r: Expr): Expr =>
    ({ k: "bin", op: op.text, l, r, line: op.line, col: op.col });

  // Left-associative chain of `next` separated by the given operators.
  const chain = (next: () => Expr, isSep: (t: Token) => boolean) => (): Expr => {
    let l = next();
    while (isSep(toks[p])) {
      const op = toks[p++];
      l = bin(op, l, next());
    }
    return l;
  };

  const primary = (): Expr => {
    const t = toks[p];
    if (t.k === "int") {
      p++;
      return { k: "int", v: t.val, line: t.line, col: t.col };
    }
    if (isOp(t, "(")) {
      p++;
      const e = or();
      const c = toks[p];
      if (!isOp(c, ")")) fail(c.line, c.col, `expected ')', found ${describe(c)}`);
      p++;
      return e;
    }
    return fail(t.line, t.col, `expected expression, found ${describe(t)}`);
  };

  const unary = (): Expr => {
    const t = toks[p];
    if (isOp(t, "-")) {
      p++;
      return { k: "un", op: "-", e: unary(), line: t.line, col: t.col };
    }
    return primary();
  };

  const mul = chain(unary, (t) => isOp(t, "*", "/", "%"));
  const add = chain(mul, (t) => isOp(t, "+", "-"));

  // At most one comparison per level: `a < b < c` leaves the second `<`
  // for the statement parser to reject.
  const compare = (): Expr => {
    const l = add();
    if (toks[p].k === "op" && COMPARE.has(toks[p].text)) {
      const op = toks[p++];
      return bin(op, l, add());
    }
    return l;
  };

  const not = (): Expr => {
    const t = toks[p];
    if (isKw(t, "not")) {
      p++;
      return { k: "un", op: "not", e: not(), line: t.line, col: t.col };
    }
    return compare();
  };

  const and = chain(not, (t) => isKw(t, "and"));
  const or = chain(and, (t) => isKw(t, "or"));

  const stmts: Stmt[] = [];
  while (toks[p].k !== "eof") {
    const t = toks[p];
    if (!isKw(t, "print") && !isKw(t, "write")) {
      fail(t.line, t.col, `expected statement, found ${describe(t)}`);
    }
    p++;
    stmts.push({ k: t.text as "print" | "write", e: or(), line: t.line, col: t.col });
  }
  return { k: "program", stmts };
}
