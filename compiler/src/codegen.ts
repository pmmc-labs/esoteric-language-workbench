import type { Expr, Program, Stmt } from "./parser.ts";

const BIN: Record<string, string> = {
  "+": "add", "-": "sub", "*": "mul", "/": "div", "%": "mod",
  "=": "eq", "!=": "ne", "<": "lt", "<=": "le", ">": "gt", ">=": "ge",
};

// Every subexpression goes into a fresh temporary, in source order (D25).
// Every value is a history (D11), so a literal is a one-layer history.
// Runtime calls only ever see temporaries, so C's unspecified argument
// order can't matter. `and`/`or` are an `if` around the right side so it
// runs only when needed (D20). A `while` condition's temporaries sit inside
// the loop, so they are computed again each round (D38).
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
    if (e.k === "name") {
      // A copy of the pointer, so a later write to the variable can't
      // change what this operand already read (D25).
      const t = fresh();
      emit(`strata_hist ${t} = v_${e.name};`);
      return t;
    }
    if (e.k === "list") {
      // Elements first, in source order; then they are laid oldest first.
      const ts = e.elems.map(expr);
      const t = fresh();
      emit(`strata_hist ${t} = NULL;`);
      for (const a of ts) emit(`${t} = strata_lay(${t}, ${a}, ${e.line}, ${e.col});`);
      return t;
    }
    if (e.k === "at") {
      const a = expr(e.e);
      const i = expr(e.i);
      const t = fresh();
      emit(`strata_hist ${t} = strata_at(${a}, ${i}, ${e.line}, ${e.col});`);
      return t;
    }
    if (e.k === "un") {
      const a = expr(e.e);
      const t = fresh();
      const fn = { "-": "neg", "not": "not", "#": "depth" }[e.op];
      emit(`strata_hist ${t} = strata_${fn}(${a}, ${e.line}, ${e.col});`);
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

  // A block is a C block: a `let` in it is a C local, so each round of a
  // loop gets a fresh one (D14), and a name is gone at the closing brace.
  const block = (body: Stmt[]) => {
    depth++;
    body.forEach(stmt);
    depth--;
  };

  const stmt = (s: Stmt): void => {
    if (s.k === "if") {
      const c = expr(s.cond);
      emit(`if (strata_truth(${c}, ${s.line}, ${s.col})) {`);
      block(s.then);
      if (s.els) {
        emit("} else {");
        block(s.els);
      }
      emit("}");
    } else if (s.k === "while") {
      emit("for (;;) {");
      depth++;
      const c = expr(s.cond);
      emit(`if (!strata_truth(${c}, ${s.line}, ${s.col})) break;`);
      depth--;
      block(s.body);
      emit("}");
    } else {
      const t = expr(s.e);
      if (s.k === "let") emit(`strata_hist v_${s.name} = ${t};`);
      else if (s.k === "set") emit(`v_${s.name} = strata_lay(v_${s.name}, ${t}, ${s.line}, ${s.col});`);
      else emit(`strata_${s.k}(${t}, ${s.line}, ${s.col});`);
    }
  };

  prog.stmts.forEach(stmt);
  return `#include "strata.h"\n\nint main(void) {\n${out.join("\n")}\n  return 0;\n}\n`;
}
