// The evaluator: a tree-walker over the checker's nodes (D29). A value is
// a bigint (an integer, kept in 63 bits: D4) or a JS boolean (D11).
// Left to right (D25): an operator's left operand, then its right, then
// the operator.
import type { Node, Value } from "./checker.ts";
import { ops } from "./ops.ts";

export function evaluate(n: Node): Value {
  switch (n.kind) {
    case "lit": return n.value;
    case "op": {
      const a = evaluate(n.a);
      const b = evaluate(n.b);
      return ops.get(n.name)!(a, b);
    }
  }
}

export const show = (v: Value): string => (typeof v === "boolean" ? (v ? "#true" : "#false") : v.toString());
