import type { Expr, Program } from "./parser.ts";

// Every subexpression goes into a fresh temporary, in source order (D25).
// Every value is a history (D11), so a literal is a one-layer history.
export function codegen(prog: Program): string {
  const out: string[] = [];
  let tmp = 0;
  const expr = (e: Expr): string => {
    const t = `t${++tmp}`;
    out.push(`  strata_hist ${t} = strata_num(INT64_C(${e.v}));`);
    return t;
  };
  for (const s of prog.stmts) {
    const t = expr(s.e);
    out.push(`  strata_print(${t}, ${s.line}, ${s.col});`);
  }
  return `#include "strata.h"\n\nint main(void) {\n${out.join("\n")}\n  return 0;\n}\n`;
}
