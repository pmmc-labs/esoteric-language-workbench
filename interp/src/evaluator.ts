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

// The budget (D21 to D24), as two counts: `spent`, the operations done
// since the program started, and `limit`, the count at which the next is
// refused. Every limit is a count from the start, so the innermost is
// the lowest and checking one checks every budget in force (D23).
type Budget = { spent: bigint; limit: bigint };
const NO_LIMIT = 1n << 64n;

// D34: calls in progress, not counting tail calls (D33).
export const MAX_CALLS = 10_000;

export type Fn = { params: string[]; body: Form };
export type Program = { fns: Map<string, Fn>; main: Form };

type List = Extract<Form, { t: "list" }>;
type Env = Map<string, Value>;
// The work still to do, on a stack of the evaluator's own: nothing a
// program does recurses on the host's stack (D34). `ret` marks a call in
// progress; a call with `ret` on top of the stack has nothing left to do
// after it, which is a tail call (D33). Anything else waiting (an
// operator, an `if`'s test, a `within`'s restore) means it isn't one.
type Task =
  | { k: "ev"; f: Form; env: Env }
  | { k: "op"; f: List }
  | { k: "if"; f: List; env: Env }
  | { k: "within"; f: List; env: Env }
  | { k: "restore"; limit: bigint }
  | { k: "call"; fn: Fn }
  | { k: "ret" };
const RET: Task = { k: "ret" };

export function evaluate(p: Program): Value {
  const b: Budget = { spent: 0n, limit: NO_LIMIT };
  const tasks: Task[] = [{ k: "ev", f: p.main, env: new Map() }];
  const vals: Value[] = [];
  let depth = 0;
  while (tasks.length) {
    const t = tasks.pop()!;
    switch (t.k) {
      case "ev": {
        const f = t.f;
        if (f.t === "int" || f.t === "bool") vals.push(f.v);
        else if (f.t === "sym") vals.push(t.env.get(f.name)!);
        else if (f.t === "list") {
          const name = (f.items[0] as { name: string }).name;
          // The operands go on the stack last first, so the left comes off
          // first (D25), written out rather than leaned on.
          const operands = (from: number, task: Task) => {
            tasks.push(task);
            for (let i = f.items.length - 1; i >= from; i--) tasks.push({ k: "ev", f: f.items[i], env: t.env });
          };
          if (name === "if") {
            // Only the taken branch is evaluated (D13). Not an operation.
            tasks.push({ k: "if", f, env: t.env });
            tasks.push({ k: "ev", f: f.items[1], env: t.env });
          } else if (name === "within") {
            // The budget first, under the budgets already in force (D24).
            tasks.push({ k: "within", f, env: t.env });
            tasks.push({ k: "ev", f: f.items[1], env: t.env });
          } else if (OPERATORS.has(name)) operands(1, { k: "op", f });
          else operands(1, { k: "call", fn: p.fns.get(name)! });
        } else throw new Error("evaluate: unchecked form");
        break;
      }
      case "if": {
        const test = vals.pop()!;
        if (typeof test !== "boolean") throw new Fault("not a boolean");
        // Pushed after the `if` is gone, so a call in a branch of an `if`
        // in tail position finds `ret` on top (D33).
        tasks.push({ k: "ev", f: t.f.items[test ? 2 : 3], env: t.env });
        break;
      }
      case "within": {
        const n = vals.pop()!;
        if (typeof n !== "bigint") throw new Fault("not an integer");
        if (n < 0n) throw new Fault("bad budget");
        // What the body didn't use is dropped; the outer has seen every
        // operation through `spent`. Not a tail position (D33): the
        // restore is work left after the body.
        tasks.push({ k: "restore", limit: b.limit });
        if (n < b.limit - b.spent) b.limit = b.spent + n;
        tasks.push({ k: "ev", f: t.f.items[2], env: t.env });
        break;
      }
      case "restore":
        b.limit = t.limit;
        break;
      case "op": {
        const y = vals.pop()!, x = vals.pop()!;
        // Charged after the operands, before the operator's own checks (D22).
        if (b.spent === b.limit) throw new Fault("budget spent");
        b.spent++;
        vals.push(OPERATORS.get((t.f.items[0] as { name: string }).name)!(x, y));
        break;
      }
      case "call": {
        const args = vals.splice(vals.length - t.fn.params.length);
        // The charge (D32), then the depth (D34), then the body.
        if (b.spent === b.limit) throw new Fault("budget spent");
        b.spent++;
        if (tasks[tasks.length - 1] !== RET) {
          if (depth === MAX_CALLS) throw new Fault("stack");
          depth++;
          tasks.push(RET);
        }
        const env: Env = new Map();
        t.fn.params.forEach((n, i) => env.set(n, args[i]));
        tasks.push({ k: "ev", f: t.fn.body, env });
        break;
      }
      case "ret":
        depth--;
        break;
    }
  }
  return vals.pop()!;
}

export function show(v: Value): string {
  return typeof v === "boolean" ? (v ? "#true" : "#false") : String(v);
}
