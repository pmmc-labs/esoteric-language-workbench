import { fail } from "./errors.ts";
import type { Token } from "./lexer.ts";

// line, col is where a fault in the operation is reported (D23): the
// operator token for operators.
export type Expr =
  | { k: "int"; v: string; line: number; col: number }
  | { k: "name"; name: string; line: number; col: number }
  | { k: "list"; elems: Expr[]; line: number; col: number }
  | { k: "at"; e: Expr; i: Expr; line: number; col: number }
  | { k: "bin"; op: string; l: Expr; r: Expr; line: number; col: number }
  | { k: "un"; op: string; e: Expr; line: number; col: number };
// `let` and `<-` carry the name's own position (resolve errors point at it);
// a write also carries the `<-` position, where it faults (D23).
// `if` and `while` carry the keyword's position, where a fault in the
// condition is reported (D23). `else if` is an `if` inside the else block:
// no separate form (D38).
export type Stmt =
  | { k: "print" | "write"; e: Expr; line: number; col: number }
  | { k: "let"; name: string; e: Expr; line: number; col: number }
  | { k: "set"; name: string; e: Expr; line: number; col: number; nline: number; ncol: number }
  | { k: "if"; cond: Expr; then: Stmt[]; els: Stmt[] | null; line: number; col: number }
  | { k: "while"; cond: Expr; body: Stmt[]; line: number; col: number };
export type Program = { k: "program"; stmts: Stmt[] };

// What a token is called in "expected THING, found TOKEN" (D33).
const describe = (t: Token) => (t.k === "eof" ? "end of file" : `'${t.text}'`);

const COMPARE = new Set(["=", "!=", "<", "<=", ">", ">="]);

// Precedence, loosest to tightest (LANGUAGE.md, Expressions): or, and,
// not, one comparison, + -, * / %, prefix - and #, postfix @. Each level is
// a function.
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
    if (t.k === "name") {
      p++;
      return { k: "name", name: t.text, line: t.line, col: t.col };
    }
    if (isOp(t, "[")) {
      p++;
      const elems: Expr[] = [];
      if (!isOp(toks[p], "]")) {
        elems.push(or());
        while (isOp(toks[p], ",")) { p++; elems.push(or()); }
      }
      const c = toks[p];
      if (!isOp(c, "]")) fail(c.line, c.col, `expected ']', found ${describe(c)}`);
      p++;
      return { k: "list", elems, line: t.line, col: t.col };
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

  // `e@k` chains left; k is a primary, so `x@1@1` is `(x@1)@1` and
  // `x@-1` is a parse error (D13).
  const postfix = (): Expr => {
    let e = primary();
    while (isOp(toks[p], "@")) {
      const at = toks[p++];
      e = { k: "at", e, i: primary(), line: at.line, col: at.col };
    }
    return e;
  };

  const unary = (): Expr => {
    const t = toks[p];
    if (isOp(t, "-", "#")) {
      p++;
      return { k: "un", op: t.text, e: unary(), line: t.line, col: t.col };
    }
    return postfix();
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

  const expect = (what: string, ok: (t: Token) => boolean): Token => {
    const t = toks[p];
    if (!ok(t)) fail(t.line, t.col, `expected ${what}, found ${describe(t)}`);
    p++;
    return t;
  };

  // A block is the body of an if, else or while (D38). Its statements end
  // at the `}`; a file that ends first is reported at the end of file.
  const block = (): Stmt[] => {
    expect("'{'", (x) => isOp(x, "{"));
    const body: Stmt[] = [];
    while (!isOp(toks[p], "}")) {
      if (toks[p].k === "eof") fail(toks[p].line, toks[p].col, "expected '}', found end of file");
      body.push(stmt());
    }
    p++;
    return body;
  };

  // `t` is the `if` keyword, already consumed by the caller's check.
  const ifRest = (t: Token): Stmt => {
    p++;
    const cond = or();
    const then = block();
    let els: Stmt[] | null = null;
    if (isKw(toks[p], "else")) {
      p++;
      if (isKw(toks[p], "if")) els = [ifRest(toks[p])];
      else els = block();
    }
    return { k: "if", cond, then, els, line: t.line, col: t.col };
  };

  const stmt = (): Stmt => {
    const t = toks[p];
    if (isKw(t, "print") || isKw(t, "write")) {
      p++;
      return { k: t.text as "print" | "write", e: or(), line: t.line, col: t.col };
    }
    if (isKw(t, "let")) {
      p++;
      const n = expect("name", (x) => x.k === "name");
      expect("'='", (x) => isOp(x, "="));
      return { k: "let", name: n.text, e: or(), line: n.line, col: n.col };
    }
    if (t.k === "name") {
      p++;
      const arrow = expect("'<-'", (x) => isOp(x, "<-"));
      return { k: "set", name: t.text, e: or(), line: arrow.line, col: arrow.col,
        nline: t.line, ncol: t.col };
    }
    if (isKw(t, "if")) return ifRest(t);
    if (isKw(t, "while")) {
      p++;
      const cond = or();
      return { k: "while", cond, body: block(), line: t.line, col: t.col };
    }
    return fail(t.line, t.col, `expected statement, found ${describe(t)}`);
  };

  const stmts: Stmt[] = [];
  while (toks[p].k !== "eof") stmts.push(stmt());
  return { k: "program", stmts };
}
