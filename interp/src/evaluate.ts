// The evaluator: a tree-walker over checked forms (D29). A value is a bigint for
// an integer and a boolean for a boolean (D31).
import type { Form } from './reader.ts';

export type Value = bigint | boolean;

export function evaluate(f: Form): Value {
  switch (f.kind) {
    case 'int':
      return f.value;
    case 'bool':
      return f.value;
    default:
      // The checker has already refused every other form; reaching here is a bug in
      // the interpreter, which the driver reports as an internal error (D34).
      throw new Error(`no evaluation for ${f.kind} yet`);
  }
}

// Printed as the language writes them: `typeof` is the tag, and the boolean is
// spelled out, since String(true) isn't `#true` (D11, DESIGN.md's printing line).
export function show(v: Value): string {
  return typeof v === 'bigint' ? v.toString() : v ? '#true' : '#false';
}
