// The evaluator: a tree-walker over checked forms (D29). A value is a
// bigint (the integers of D4), a boolean (D11) or a string (D31). A
// string's characters are its code points, never the host's UTF-16 units,
// so the string operators count and compare code points (D33).

import { Fault } from "./errors.ts";
import { MIN, MAX } from "./reader.ts";
import type { Form } from "./reader.ts";

export type Value = bigint | boolean | string;
// An operator's arity, and its function. The function gets its operands
// already evaluated, and does its checks in the order the decisions give.
export type Op = { arity: 1 | 2; fn: (...a: Value[]) => Value };

// The range check of D4: every integer result goes through it.
const fit = (x: bigint): bigint => {
  if (x < MIN || x > MAX) throw new Fault("overflow");
  return x;
};

// Both operands must be integers (D11, D17); this is each operator's
// first check, so a boolean is reported before any other fault.
const ints = (f: (a: bigint, b: bigint) => Value) => (a: Value, b: Value): Value => {
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

// A string's operand, checked for its type (D33): "not a string".
const str = (v: Value): string => {
  if (typeof v !== "string") throw new Fault("not a string");
  return v;
};

// An integer operand: "not an integer", as the arithmetic gives (D33).
const int = (v: Value): bigint => {
  if (typeof v !== "bigint") throw new Fault("not an integer");
  return v;
};

// The code points of a string, one number each. `[...s]` steps by code
// point, so a character past U+FFFF is one of them, not two (D31).
const points = (s: string): number[] => [...s].map((c) => c.codePointAt(0)!);

// Code point by code point, and a prefix before what it begins (D33).
const lessThan = (x: number[], y: number[]): boolean => {
  for (let k = 0; k < Math.min(x.length, y.length); k++)
    if (x[k] !== y[k]) return x[k] < y[k];
  return x.length < y.length;
};

const bin = (fn: (a: Value, b: Value) => Value): Op => ({ arity: 2, fn });
const un = (fn: (a: Value) => Value): Op => ({ arity: 1, fn });

export const OPERATORS: Map<string, Op> = new Map([
  ["+", bin(ints((a, b) => fit(a + b)))],
  ["-", bin(ints((a, b) => fit(a - b)))],
  ["*", bin(ints((a, b) => fit(a * b)))],
  // bigint / and % truncate toward zero, remainder with the dividend's
  // sign, which is D5; only the zero divisor is ours to catch.
  ["<", bin(ints((a, b) => a < b))],
  ["<=", bin(ints((a, b) => a <= b))],
  [">", bin(ints((a, b) => a > b))],
  [">=", bin(ints((a, b) => a >= b))],
  // typeof first and === only: JS's == would coerce (D12). On strings,
  // === compares code units, which is code points for every string here
  // (DESIGN.md, "What the host gives").
  ["==", bin((a, b) => a === b)],
  ["!=", bin((a, b) => a !== b)],
  // bigint & | ^ are two's complement at any width, which is D15.
  ["bit/and", bin(ints((a, b) => a & b))],
  ["bit/or", bin(ints((a, b) => a | b))],
  ["bit/xor", bin(ints((a, b) => a ^ b))],
  // The types are checked first, then the count, then the result: where
  // one application could fault two ways, the order is open (CLAUDE.md's
  // Status), and this is the interpreter's.
  ["bit/shl", bin(ints((a, n) => fit(a << shiftCount(n))))],
  ["bit/shr", bin(ints((a, n) => a >> shiftCount(n)))],
  ["**", bin(ints(power))],
  ["/", bin(ints((a, b) => { if (b === 0n) throw new Fault("division by zero"); return fit(a / b); }))],
  ["%", bin(ints((a, b) => { if (b === 0n) throw new Fault("division by zero"); return a % b; }))],
  // The six string operators (D33). Each checks its operands left to
  // right for their types, then the index or code point for its range.
  ["str/len", un((s) => BigInt(points(str(s)).length))],
  ["str/code", un((s) => {
    const cs = points(str(s));
    if (cs.length !== 1) throw new Fault("not a character");
    return BigInt(cs[0]);
  })],
  ["str/char", un((n) => {
    const k = int(n);
    if (k < 0n || k > 0x10ffffn || (k >= 0xd800n && k <= 0xdfffn)) throw new Fault("not a character");
    return String.fromCodePoint(Number(k));
  })],
  ["str/at", bin((s, i) => {
    const t = str(s);
    const k = int(i);
    const cs = points(t);
    if (k < 0n || k >= BigInt(cs.length)) throw new Fault("bad index");
    return String.fromCodePoint(cs[Number(k)]);
  })],
  ["str/cat", bin((a, b) => str(a) + str(b))],
  ["str/lt", bin((a, b) => {
    const x = points(str(a));
    return lessThan(x, points(str(b)));
  })],
]);

// The budget (D21 to D24), as two counts: `spent`, the operations done
// since the program started, and `limit`, the count at which the next is
// refused. Every limit is a count from the start, so the innermost is
// the lowest and checking one checks every budget in force (D23).
type Budget = { spent: bigint; limit: bigint };
const NO_LIMIT = 1n << 64n;

export function evaluate(f: Form): Value {
  return ev(f, { spent: 0n, limit: NO_LIMIT });
}

function ev(f: Form, b: Budget): Value {
  switch (f.t) {
    case "int":
    case "bool":
    case "str":
      return f.v;
    case "list": {
      const name = (f.items[0] as { name: string }).name;
      if (name === "if") {
        // Only the taken branch is evaluated (D13). Not an operation.
        const test = ev(f.items[1], b);
        if (typeof test !== "boolean") throw new Fault("not a boolean");
        return ev(f.items[test ? 2 : 3], b);
      }
      if (name === "within") {
        // The budget is evaluated first, under the budgets already in
        // force (D24), then checked, then the body runs under the new one.
        const n = ev(f.items[1], b);
        if (typeof n !== "bigint") throw new Fault("not an integer");
        if (n < 0n) throw new Fault("bad budget");
        const saved = b.limit;
        if (n < b.limit - b.spent) b.limit = b.spent + n;
        const v = ev(f.items[2], b);
        // What the body didn't use is dropped; the outer has seen every
        // operation through `spent`.
        b.limit = saved;
        return v;
      }
      const op = OPERATORS.get(name)!;
      // The operands completely, left to right (D25, D33), then the
      // charge, then the operator's own checks (D22).
      const args: Value[] = [];
      for (let k = 1; k <= op.arity; k++) args.push(ev(f.items[k], b));
      if (b.spent === b.limit) throw new Fault("budget spent");
      b.spent++;
      return op.fn(...args);
    }
    default:
      throw new Error(`evaluate: unchecked form ${f.t}`);
  }
}

export function show(v: Value): string {
  if (typeof v === "boolean") return v ? "#true" : "#false";
  if (typeof v === "string") return quote(v);
  return String(v);
}

// How a string prints (D32), a code point at a time, so that what prints
// reads back as the same string: the escapes of D32, and everything else
// as itself, the C1 controls and U+2028 among it.
function quote(s: string): string {
  let o = '"';
  for (const c of s) {
    const cp = c.codePointAt(0)!;
    if (c === '"') o += '\\"';
    else if (c === "\\") o += "\\\\";
    else if (c === "\n") o += "\\n";
    else if (c === "\t") o += "\\t";
    else if (cp < 0x20 || cp === 0x7f) o += `\\u{${cp.toString(16)}}`;
    else o += c;
  }
  return o + '"';
}
