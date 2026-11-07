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
  if (typeof a !== 'bigint' || typeof b !== 'bigint') throw new Fault('not an integer');
  switch (op) {
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
    default:
      throw new Error(`no operator ${op}`);
  }
}

// Printed as the language writes them. String(true) isn't `#true`, so a boolean is
// spelled out (D11).
export function show(v: Value): string {
  return typeof v === 'bigint' ? v.toString() : v ? '#true' : '#false';
}
