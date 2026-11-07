import type { Expr, Program } from "./parser.ts";

const BIN: Record<string, string> = {
  "+": "add", "-": "sub", "*": "mul", "/": "div", "%": "mod",
  "=": "eq", "!=": "ne", "<": "lt", "<=": "le", ">": "gt", ">=": "ge",
};

// Every subexpression goes into a fresh temporary, in source order (D25).
// Every value is a history (D11), so a literal is a one-layer history.
// Runtime calls only ever see temporaries, so C's unspecified argument
// order can't matter. `and`/`or` are an `if` around the right side so it
// runs only when needed (D20).
export function codegen(prog: Program): string {
  const out: string[] = [];
  let tmp = 0;
  let depth = 1;
  const emit = (s: string) => out.push("  ".repeat(depth) + s);
  const fresh = () => `t${++tmp}`;

  const expr = (e: Expr): string => {
    if (e.k === "int") {
      const t = fresh();
      emit(`strata_hist ${t} = strata_num(INT64_C(${e.v}));`);
      return t;
    }
    if (e.k === "un") {
      const a = expr(e.e);
      const t = fresh();
      emit(`strata_hist ${t} = strata_${e.op === "-" ? "neg" : "not"}(${a}, ${e.line}, ${e.col});`);
      return t;
    }
    if (e.op === "and" || e.op === "or") return logic(e);
    const a = expr(e.l);
    const b = expr(e.r);
    const t = fresh();
    emit(`strata_hist ${t} = strata_${BIN[e.op]}(${a}, ${b}, ${e.line}, ${e.col});`);
    return t;
  };

  // `a and b`: 0 if a is false, else b's truth. `a or b`: 1 if a is true,
  // else b's truth. The result is a fresh 1/0 history either way.
  const logic = (e: Extract<Expr, { k: "bin" }>): string => {
    const isAnd = e.op === "and";
    const a = expr(e.l);
    const t = fresh();
    emit(`strata_hist ${t};`);
    emit(`if (${isAnd ? "" : "!"}strata_truth(${a}, ${e.line}, ${e.col})) {`);
    depth++;
    const b = expr(e.r);
    const v = fresh();
    emit(`int ${v} = strata_truth(${b}, ${e.line}, ${e.col});`);
    emit(`${t} = strata_num(${v});`);
    depth--;
    emit(`} else {`);
    depth++;
    emit(`${t} = strata_num(${isAnd ? 0 : 1});`);
    depth--;
    emit(`}`);
    return t;
  };

  for (const s of prog.stmts) {
    const t = expr(s.e);
    emit(`strata_${s.k}(${t}, ${s.line}, ${s.col});`);
  }
  return `#include "strata.h"\n\nint main(void) {\n${out.join("\n")}\n  return 0;\n}\n`;
}
