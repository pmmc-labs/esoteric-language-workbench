// The evaluator: a tree-walker over checked forms (D29). A value is a
// bigint (the integers of D4) or a boolean (D11).

import type { Form } from "./reader.ts";

export type Value = bigint | boolean;

export function evaluate(f: Form): Value {
  if (f.t === "int") return f.v;
  throw new Error(`evaluate: unchecked form ${f.t}`);
}

export function show(v: Value): string {
  return typeof v === "boolean" ? (v ? "#true" : "#false") : String(v);
}
