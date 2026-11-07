// The evaluator: a tree-walker over checked forms (D29), run as a loop
// over a stack of its own, so no program call is a host call (D34, and
// the tail calls of D33 need no host support). A value is a bigint (the
// integers of D4) or a boolean (D11).

import { Fault } from "./errors.ts";
import { MIN, MAX } from "./reader.ts";
import type { Form, ListForm } from "./reader.ts";
import type { Def, Program } from "./checker.ts";

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

// Calls in progress that a program may have (D34): the call that would be
// the 10,001st faults `stack`.
export const MAX_CALLS = 10000;

// The budget (D21 to D24), as two counts: `spent`, the operations done
// since the program started, and `limit`, the count at which the next is
// refused. Every limit is a count from the start, so the innermost is
// the lowest and checking one checks every budget in force (D23).
const NO_LIMIT = 1n << 64n;

type Env = Map<string, Value>;

// What is waiting for a value. A frame is pushed when its sub-expression
// starts, and popped when that value comes back.
type Frame =
  | { k: "if"; f: ListForm; env: Env; tail: boolean }
  | { k: "budget"; f: ListForm; env: Env }
  | { k: "limit"; saved: bigint }
  | { k: "args"; f: ListForm; env: Env; tail: boolean; vals: Value[]; op?: (a: Value, b: Value) => Value; def?: Def }
  | { k: "return"; env: Env };

// The machine is in one of two states: evaluating `f` in `env`, or
// returning `v` to the frame on top of `stack`. `tail` says whether the
// form being evaluated is in tail position (D33): a function's body is,
// and so are the branches of an if that is; nothing else is. A call in
// tail position replaces its caller's frame, so it pushes no `return` and
// adds no depth. The program's expression is not in tail position, so a
// call from it makes depth 1 (D34).
export function evaluate(p: Program): Value {
  const stack: Frame[] = [];
  let spent = 0n, limit = NO_LIMIT;
  let depth = 0;
  let env: Env = new Map();
  let tail = false;
  let f: Form | undefined = p.expr;
  let v: Value = 0n;

  // Charged as one operation, before any check of its own (D22, D32).
  const charge = () => {
    if (spent === limit) throw new Fault("budget spent");
    spent++;
  };

  // A call whose arguments are all in: charged (D32), checked for depth
  // unless a tail call (D34), then the body runs with the parameters bound.
  // The caller's environment is saved before the new one replaces it.
  const enter = (def: Def, vals: Value[], callTail: boolean): Form => {
    charge();
    if (!callTail) {
      if (depth === MAX_CALLS) throw new Fault("stack");
      stack.push({ k: "return", env });
      depth++;
    }
    env = new Map<string, Value>(def.params.map((name, i): [string, Value] => [name, vals[i]]));
    tail = true;
    return def.body;
  };

  for (;;) {
    if (f !== undefined) {
      switch (f.t) {
        case "int":
        case "bool":
          v = f.v;
          f = undefined;
          break;
        case "sym":
          // The checker allows a name here only as a parameter in scope.
          v = env.get(f.name)!;
          f = undefined;
          break;
        case "list": {
          const name = (f.items[0] as { name: string }).name;
          // Only the taken branch is evaluated (D13). Not an operation.
          if (name === "if") {
            stack.push({ k: "if", f, env, tail });
            f = f.items[1];
            tail = false;
            break;
          }
          // The budget is evaluated first, under the budgets already in
          // force (D24), then checked, then the body runs under the new one.
          if (name === "within") {
            stack.push({ k: "budget", f, env });
            f = f.items[1];
            tail = false;
            break;
          }
          const op = OPERATORS.get(name);
          if (op) {
            // Left operand completely, then the right, then the charge,
            // then the operator's own checks (D25, D22).
            stack.push({ k: "args", f, env, tail, vals: [], op });
          } else {
            const def = p.defs.get(name)!;
            if (f.items.length === 1) {
              f = enter(def, [], tail);
              break;
            }
            // Arguments left to right, then the charge, then the body (D25, D32).
            stack.push({ k: "args", f, env, tail, vals: [], def });
          }
          f = f.items[1];
          tail = false;
          break;
        }
      }
      continue;
    }

    const fr = stack.pop();
    if (fr === undefined) return v;
    switch (fr.k) {
      case "if": {
        // The test is a boolean at run time (D13).
        if (typeof v !== "boolean") throw new Fault("not a boolean");
        env = fr.env;
        tail = fr.tail;
        f = fr.f.items[v ? 2 : 3];
        break;
      }
      case "budget": {
        if (typeof v !== "bigint") throw new Fault("not an integer");
        if (v < 0n) throw new Fault("bad budget");
        env = fr.env;
        // The body's budget is the outer one, or this one if that's lower
        // (D23). When the body ends the outer limit is put back (D24).
        const saved = limit;
        if (v < limit - spent) limit = spent + v;
        stack.push({ k: "limit", saved });
        f = fr.f.items[2];
        tail = false;
        break;
      }
      case "limit":
        // What the body didn't use is dropped; the outer has seen every
        // operation through `spent`.
        limit = fr.saved;
        break;
      case "args": {
        fr.vals.push(v);
        env = fr.env;
        const n = fr.f.items.length - 1;
        if (fr.vals.length < n) {
          stack.push(fr);
          f = fr.f.items[fr.vals.length + 1];
          tail = false;
          break;
        }
        if (fr.op) {
          charge();
          v = fr.op(fr.vals[0], fr.vals[1]);
          break;
        }
        f = enter(fr.def!, fr.vals, fr.tail);
        break;
      }
      case "return":
        env = fr.env;
        depth--;
        break;
    }
  }
}

export function show(v: Value): string {
  return typeof v === "boolean" ? (v ? "#true" : "#false") : String(v);
}
