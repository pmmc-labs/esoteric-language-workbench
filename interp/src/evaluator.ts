// The evaluator: a tree-walker over checked forms (D29). A value is a
// bigint (the integers of D4) or a boolean (D11).

import { Fault } from "./errors.ts";
import { MIN, MAX } from "./reader.ts";
import type { Form } from "./reader.ts";

export type Value = bigint | boolean;
type Op = (a: Value, b: Value) => Value;

// The range check of D4: every integer result goes through it.
const fit = (x: bigint): bigint => {
  if (x < MIN || x > MAX) throw new Fault("overflow");
  return x;
};

// Both operands must be integers (D11, D17); this is each operator's
// first check, so a boolean is reported before any other fault.
const ints = (f: (a: bigint, b: bigint) => bigint): Op => (a, b) => {
  if (typeof a !== "bigint" || typeof b !== "bigint") throw new Fault("not an integer");
  return f(a, b);
};

export const OPERATORS: Map<string, Op> = new Map([
  ["+", ints((a, b) => fit(a + b))],
  ["-", ints((a, b) => fit(a - b))],
  ["*", ints((a, b) => fit(a * b))],
  // bigint / and % truncate toward zero, remainder with the dividend's
  // sign, which is D5; only the zero divisor is ours to catch.
  ["/", ints((a, b) => { if (b === 0n) throw new Fault("division by zero"); return fit(a / b); })],
  ["%", ints((a, b) => { if (b === 0n) throw new Fault("division by zero"); return a % b; })],
]);

export function evaluate(f: Form): Value {
  switch (f.t) {
    case "int":
      return f.v;
    case "list": {
      const op = OPERATORS.get((f.items[0] as { name: string }).name)!;
      // Left operand completely, then the right, then the operator (D25).
      const a = evaluate(f.items[1]);
      const b = evaluate(f.items[2]);
      return op(a, b);
    }
    default:
      throw new Error(`evaluate: unchecked form ${f.t}`);
  }
}

export function show(v: Value): string {
  return typeof v === "boolean" ? (v ? "#true" : "#false") : String(v);
}
