// The evaluator: a tree-walker over the checker's nodes (D29). A value is
// a bigint (an integer, kept in 63 bits: D4) or a JS boolean (D11).
import type { Node, Value } from "./checker.ts";

export function evaluate(n: Node): Value {
  return n.value;
}

export const show = (v: Value): string => (typeof v === "boolean" ? (v ? "#true" : "#false") : v.toString());
