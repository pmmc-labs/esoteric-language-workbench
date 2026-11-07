// What each operator takes (D3: exactly two operands each). A Map and not an
// object, so a head named `constructor` or `toString` isn't an operator.
export const ARITY = new Map<string, number>([
  ['+', 2],
  ['-', 2],
  ['*', 2],
  ['/', 2],
  ['%', 2],
  ['<', 2],
  ['<=', 2],
  ['>', 2],
  ['>=', 2],
  ['==', 2],
  ['!=', 2],
  // A special form, not an operator: it evaluates only the branch taken (D13).
  ['if', 3],
]);
