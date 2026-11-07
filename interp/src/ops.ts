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

// D12: an ordering on a non-integer faults; == and != take any two values,
// and values of different types are unequal (=== on a bigint and a boolean).
const ord = (f: (a: bigint, b: bigint) => boolean) => (a: Value, b: Value): Value => f(...ints(a, b));

// D16: a shift count is checked, 0 to 62, never masked. When one
// application could fault two ways (a boolean and a bad count) the
// interpreter reports `not an integer`: operands' types first, then the
// operator's own checks. Not agreed (CLAUDE.md's Status), and no test has one.
const shift = (f: (a: bigint, n: bigint) => bigint) =>
  int2((a, n) => f(a, n >= 0n && n <= 62n ? n : bad("bad shift")));
const bad = (m: string): never => { throw new Fault(m); };

// D18, D19: a ** 0 is 1 whatever a is; a negative exponent faults whatever
// the base. The exponent can be as large as the range, so a base other
// than 0, 1 and -1, whose powers stay in range, is out of range by the 63rd
// power at the latest and never needs a loop that long.
const pow = (a: bigint, b: bigint): bigint => {
  if (b < 0n) throw new Fault("bad exponent");
  if (a === 0n || a === 1n) return b === 0n ? 1n : a;
  if (a === -1n) return b % 2n === 0n ? 1n : -1n;
  if (b > 62n) throw new Fault("overflow");
  return a ** b;
};

export type Op = (a: Value, b: Value) => Value;

export const ops: Map<string, Op> = new Map<string, Op>([
  ["+", int2((a, b) => a + b)],
  ["-", int2((a, b) => a - b)],
  ["*", int2((a, b) => a * b)],
  ["/", int2((a, b) => a / nonzero(b))],
  ["%", int2((a, b) => a % nonzero(b))],
  ["<", ord((a, b) => a < b)],
  ["<=", ord((a, b) => a <= b)],
  [">", ord((a, b) => a > b)],
  [">=", ord((a, b) => a >= b)],
  // D15: BigInt's & | ^ are two's complement of unbounded width, which
  // every width agrees with, and the result is always in range.
  ["bit/and", int2((a, b) => a & b)],
  ["bit/or", int2((a, b) => a | b)],
  ["bit/xor", int2((a, b) => a ^ b)],
  ["bit/shl", shift((a, n) => a << n)],
  // BigInt's >> rounds toward negative infinity, which is D16's rule.
  ["bit/shr", shift((a, n) => a >> n)],
  ["**", int2(pow)],
  ["==", (a, b) => a === b],
  ["!=", (a, b) => a !== b],
]);
