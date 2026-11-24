// The syntax tree: the one data structure the passes share (D29). Plain
// objects with a `kind`, a position on every node, and nothing changed
// after the parser has made it. Step 1 gives expressions their shape.

// Lines and columns count from 1, columns in code points.
export type Pos = { line: number; col: number };

// `text` is the literal as written, since `010` and `10` are different
// things to perl; `value` is what its digits say in decimal.
export type Int = { kind: 'int'; text: string; value: bigint; pos: Pos };

export type Expr = Int;

export type Use = { kind: 'use'; version: string; pos: Pos };

// A builtin from the table of names, applied to its arguments.
export type Call = { kind: 'call'; name: string; args: readonly Expr[]; pos: Pos };

export type Stmt = Use | Call;

// `end` is where the file ends, for a diagnostic about what isn't there.
export type Program = { kind: 'program'; body: readonly Stmt[]; end: Pos };
