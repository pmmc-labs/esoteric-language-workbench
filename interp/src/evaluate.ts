// The evaluator: a tree-walker over checked forms (D29). A value is a bigint for
// an integer and a boolean for a boolean (D31).
import { Fault } from './errors.ts';
import { INT_MAX, INT_MIN, type Form } from './reader.ts';

export type Value = bigint | boolean;

export function evaluate(f: Form): Value {
  switch (f.kind) {
    case 'int':
      return f.value;
    case 'bool':
      return f.value;
    case 'list': {
      // The checker has made sure of the shape: an operator, then its operands.
      const head = f.items[0];
      if (head?.kind !== 'sym') throw new Error('a list that the checker let through has no operator');
      // `if` evaluates its test, then only the branch the test picks (D13).
      if (head.name === 'if') {
        const test = evaluate(f.items[1]!);
        if (typeof test !== 'boolean') throw new Fault('not a boolean');
        return evaluate(f.items[test ? 2 : 3]!);
      }
      // Left operand completely, then right, then the operator (D25).
      const a = evaluate(f.items[1]!);
      const b = evaluate(f.items[2]!);
      return operate(head.name, a, b);
    }
    default:
      // The checker has already refused every name; reaching here is a bug in the
      // interpreter, which the driver reports as an internal error (D34).
      throw new Error(`no evaluation for ${f.kind}`);
  }
}

// The 63-bit range (D4): a result outside it is the fault `overflow`.
function fit(v: bigint): bigint {
  if (v < INT_MIN || v > INT_MAX) throw new Fault('overflow');
  return v;
}

// The order of the faults within one application (D32): the operands' types, then
// the operator's own check, then the range of the result.
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
