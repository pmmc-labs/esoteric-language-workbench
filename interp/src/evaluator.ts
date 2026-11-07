// The evaluator: a tree-walker over the checker's nodes (D29). A value is
// a bigint (an integer, kept in 63 bits: D4) or a JS boolean (D11).
// Left to right (D25): an operator's left operand, then its right, then
// the operator; an if's test, then one branch; a within's budget, then
// its body.
import type { Node, Value } from "./checker.ts";
import { Fault } from "./errors.ts";
import { ops } from "./ops.ts";

// The budgets (D21 to D24), kept as D27 keeps them though the mechanism
// is ours (D28): `spent` is the operations done since the program started
// and `limit` the count at which the next is refused, at first none. Both
// are counts from the start, so the innermost budget is the lowest limit
// and one comparison checks every budget in force (D23); an inner
// within's end has only to put the outer's limit back, the outer having
// seen every operation through `spent`. Numbers, not bigints: `spent` would
// need 2^53 operations to lose precision, and a budget's n past that is
// only ever compared against it.
type Budget = { spent: number; limit: number };

export function evaluate(n: Node, budget: Budget = { spent: 0, limit: Infinity }): Value {
  switch (n.kind) {
    case "lit": return n.value;
    case "op": {
      const a = evaluate(n.a, budget);
      const b = evaluate(n.b, budget);
      // D22: charged after the operands, before the operator checks anything.
      if (budget.spent >= budget.limit) throw new Fault("budget spent");
      budget.spent++;
      return ops.get(n.name)!(a, b);
    }
    case "if": {
      // D13: no truthiness, and only the taken branch is evaluated.
      const t = evaluate(n.test, budget);
      if (typeof t !== "boolean") throw new Fault("not a boolean");
      return evaluate(t ? n.then : n.else, budget);
    }
    case "within": {
      // D24: the budget is evaluated first, under the budgets already in
      // force, then checked, then the body runs under the new one.
      const v = evaluate(n.budget, budget);
      if (typeof v !== "bigint") throw new Fault("not an integer");
      if (v < 0n) throw new Fault("bad budget");
      const saved = budget.limit;
      budget.limit = Math.min(saved, budget.spent + Number(v));
      const r = evaluate(n.body, budget);
      budget.limit = saved;
      return r;
    }
  }
}

export const show = (v: Value): string => (typeof v === "boolean" ? (v ? "#true" : "#false") : v.toString());
