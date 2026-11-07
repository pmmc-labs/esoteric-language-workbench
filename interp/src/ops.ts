// The operators: name to function on two values. The checker asks `ops.has`
// for what is an operator; the evaluator applies them. A Map, since a
// plain object would make `toString` an operator.
import { Fault } from "./errors.ts";
import { MIN, MAX } from "./reader.ts";
import type { Value } from "./checker.ts";

// D4: a result that doesn't fit 63 bits faults.
const fit = (n: bigint): bigint => {
  if (n < MIN || n > MAX) throw new Fault("overflow");
  return n;
};

// D11: arithmetic on a non-integer faults, whichever operand it is.
const ints = (a: Value, b: Value): [bigint, bigint] => {
  if (typeof a !== "bigint" || typeof b !== "bigint") throw new Fault("not an integer");
  return [a, b];
};

const int2 = (f: (a: bigint, b: bigint) => bigint) => (a: Value, b: Value): Value => fit(f(...ints(a, b)));

// D5: BigInt's / truncates toward zero and % takes the dividend's sign.
const nonzero = (b: bigint): bigint => {
  if (b === 0n) throw new Fault("division by zero");
  return b;
};

export type Op = (a: Value, b: Value) => Value;

export const ops: Map<string, Op> = new Map<string, Op>([
  ["+", int2((a, b) => a + b)],
  ["-", int2((a, b) => a - b)],
  ["*", int2((a, b) => a * b)],
  ["/", int2((a, b) => a / nonzero(b))],
  ["%", int2((a, b) => a % nonzero(b))],
]);
