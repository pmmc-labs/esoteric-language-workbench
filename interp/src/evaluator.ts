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
const ints = (f: (a: bigint, b: bigint) => Value): Op => (a, b) => {
  if (typeof a !== "bigint" || typeof b !== "bigint") throw new Fault("not an integer");
  return f(a, b);
};

// A count outside 0 to 62 is a fault before any bigint shift is taken
// (D16): bigint << by a negative count shifts the other way.
const shiftCount = (n: bigint): bigint => {
  if (n < 0n || n > 62n) throw new Fault("bad shift");
  return n;
};

// a ** b without a bignum intermediate that never ends: bigint ** would
// try 2 ** 4611686018427387903 (D19). The exponent is checked first, so
// (** 1 -1) faults though 1 would fit; 0, 1 and -1 are answered by the
// exponent alone; any other base is at least 2 in magnitude, and 2^63
// is past the range, so an exponent past 62 overflows without a loop.
const power = (a: bigint, b: bigint): bigint => {
  if (b < 0n) throw new Fault("bad exponent");
  if (b === 0n) return 1n;
  if (a === 0n || a === 1n) return a;
  if (a === -1n) return b % 2n === 0n ? 1n : -1n;
  if (b > 62n) throw new Fault("overflow");
  return fit(a ** b);
};

export const OPERATORS: Map<string, Op> = new Map([
  ["+", ints((a, b) => fit(a + b))],
  ["-", ints((a, b) => fit(a - b))],
  ["*", ints((a, b) => fit(a * b))],
  // bigint / and % truncate toward zero, remainder with the dividend's
  // sign, which is D5; only the zero divisor is ours to catch.
  ["<", ints((a, b) => a < b)],
  ["<=", ints((a, b) => a <= b)],
  [">", ints((a, b) => a > b)],
  [">=", ints((a, b) => a >= b)],
  // typeof first and === only: JS's == would coerce (D12).
  ["==", (a, b) => a === b],
  ["!=", (a, b) => a !== b],
  // bigint & | ^ are two's complement at any width, which is D15.
  ["bit/and", ints((a, b) => a & b)],
  ["bit/or", ints((a, b) => a | b)],
  ["bit/xor", ints((a, b) => a ^ b)],
  // The types are checked first, then the count, then the result: where
  // one application could fault two ways, the order is open (CLAUDE.md's
  // Status), and this is the interpreter's.
  ["bit/shl", ints((a, n) => fit(a << shiftCount(n)))],
  ["bit/shr", ints((a, n) => a >> shiftCount(n))],
  ["**", ints(power)],
  ["/", ints((a, b) => { if (b === 0n) throw new Fault("division by zero"); return fit(a / b); })],
  ["%", ints((a, b) => { if (b === 0n) throw new Fault("division by zero"); return a % b; })],
]);

export function evaluate(f: Form): Value {
  switch (f.t) {
    case "int":
    case "bool":
      return f.v;
    case "list": {
      const name = (f.items[0] as { name: string }).name;
      if (name === "if") {
        // Only the taken branch is evaluated (D13).
        const test = evaluate(f.items[1]);
        if (typeof test !== "boolean") throw new Fault("not a boolean");
        return evaluate(f.items[test ? 2 : 3]);
      }
      const op = OPERATORS.get(name)!;
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
