// The evaluator: a tree-walker over checked forms (D29). A value is a bigint for
// an integer and a boolean for a boolean (D31).
import { Fault } from './errors.ts';
import { INT_MAX, INT_MIN, type Form } from './reader.ts';

export type Value = bigint | boolean;

// The budget (D27): `spent` is the operations done since the program started, and
// `limit` is the count at which the next one is refused. Each `within` lowers the
// limit to what it allows and puts it back when it ends, so the innermost limit is
// the lowest and one comparison checks every budget in force (D23). With no budget
// in force the limit is the largest 64-bit integer, which `spent` never reaches.
export type Budget = { spent: bigint; limit: bigint };
const NO_BUDGET = 2n ** 63n - 1n;

export function evaluate(f: Form): Value {
  return ev(f, { spent: 0n, limit: NO_BUDGET });
}

function ev(f: Form, b: Budget): Value {
  switch (f.kind) {
    case 'int':
      return f.value;
    case 'bool':
      return f.value;
    case 'list': {
      // The checker has made sure of the shape: an operator, then its operands.
      const head = f.items[0];
      if (head?.kind !== 'sym') throw new Error('a list that the checker let through has no operator');
      // `if` evaluates its test, then only the branch the test picks (D13). It isn't
      // an operation, so it isn't charged (D21).
      if (head.name === 'if') {
        const test = ev(f.items[1]!, b);
        if (typeof test !== 'boolean') throw new Fault('not a boolean');
        return ev(f.items[test ? 2 : 3]!, b);
      }
      if (head.name === 'within') return within(f.items[1]!, f.items[2]!, b);
      // Left operand completely, then right (D25). The operator is charged after its
      // operands and before its own checks (D22, D27).
      const x = ev(f.items[1]!, b);
      const y = ev(f.items[2]!, b);
      charge(b);
      return operate(head.name, x, y);
    }
    default:
      // The checker has already refused every name; reaching here is a bug in the
      // interpreter, which the driver reports as an internal error (D34).
      throw new Error(`no evaluation for ${f.kind}`);
  }
}

// One operation: refused when the count has reached the limit, else counted (D27).
function charge(b: Budget): void {
  if (b.spent === b.limit) throw new Fault('budget spent');
  b.spent += 1n;
}

// `(within n body)`: the budget first, under the budgets already in force, and then
// checked; both before the body runs (D24). The body runs under the lower of the
// limits, and the limit is put back as it was, so what the inner budget didn't use is
// dropped and the outer one has paid for what was done (D23).
function within(nf: Form, body: Form, b: Budget): Value {
  const n = ev(nf, b);
  if (typeof n !== 'bigint') throw new Fault('not an integer');
  if (n < 0n) throw new Fault('bad budget');
  const saved = b.limit;
  if (b.spent + n < b.limit) b.limit = b.spent + n;
  const v = ev(body, b);
  b.limit = saved;
  return v;
}

// The 63-bit range (D4): a result outside it is the fault `overflow`.
function fit(v: bigint): bigint {
  if (v < INT_MIN || v > INT_MAX) throw new Fault('overflow');
  return v;
}

// The order of the faults within one application (D32): the operands' types, then
// the operator's own check, then the range of the result. The budget was charged
// before this, so it comes before all of them (D22).
function operate(op: string, a: Value, b: Value): Value {
  // Equality takes any two values (D12): two of different types are unequal, not a fault.
  if (op === '==') return a === b;
  if (op === '!=') return a !== b;
  if (typeof a !== 'bigint' || typeof b !== 'bigint') throw new Fault('not an integer');
  switch (op) {
    case '<':
      return a < b;
    case '<=':
      return a <= b;
    case '>':
      return a > b;
    case '>=':
      return a >= b;
    case '+':
      return fit(a + b);
    case '-':
      return fit(a - b);
    case '*':
      return fit(a * b);
    // BigInt's `/` truncates toward zero and `%` takes the dividend's sign, as D5 says.
    case '/':
      if (b === 0n) throw new Fault('division by zero');
      return fit(a / b);
    case '%':
      if (b === 0n) throw new Fault('division by zero');
      return fit(a % b);
    // Two's complement of any width, so these are the integers' own bits (D15) and
    // can't leave the range.
    case 'bit/and':
      return a & b;
    case 'bit/or':
      return a | b;
    case 'bit/xor':
      return a ^ b;
    // The count is checked before the shift is done, so no huge count reaches <<, and
    // the result's range after it (D16). `>>` on a bigint floors, as bit/shr says.
    case 'bit/shl':
      if (b < 0n || b > 62n) throw new Fault('bad shift');
      return fit(a << b);
    case 'bit/shr':
      if (b < 0n || b > 62n) throw new Fault('bad shift');
      return a >> b;
    case '**':
      return pow(a, b);
    default:
      throw new Error(`no operator ${op}`);
  }
}

// `**` without calling the host's on a huge exponent: Node's bigint `**` builds the
// result, and 2 to the power 2^62 can't be built. So a base of 0, 1 or -1 is answered
// from its rule (D19), and any other base to a power past 62 is past the range.
function pow(a: bigint, b: bigint): bigint {
  if (b < 0n) throw new Fault('bad exponent');
  if (b === 0n) return 1n;
  if (a === 0n || a === 1n) return a;
  if (a === -1n) return b % 2n === 0n ? 1n : -1n;
  if (b > 62n) throw new Fault('overflow');
  return fit(a ** b);
}

// Printed as the language writes them. String(true) isn't `#true`, so a boolean is
// spelled out (D11).
export function show(v: Value): string {
  return typeof v === 'bigint' ? v.toString() : v ? '#true' : '#false';
}
