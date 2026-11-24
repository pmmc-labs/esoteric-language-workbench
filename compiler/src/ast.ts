// The syntax tree: the one data structure the passes share (D29). Plain
// objects with a `kind`, a position on every node, and nothing changed
// after the parser has made it. The vocabulary starts from Crayon's
// (docs/BACKGROUND.md), which had no positions and no record of brackets.

// Lines and columns count from 1, columns in code points.
export type Pos = { line: number; col: number };

// `text` is the literal as written, since `010` and `10` are different
// things to perl; `value` is what its digits say in decimal.
export type Int = { kind: 'int'; text: string; value: bigint; pos: Pos; bracketed?: true };

// An operator before its operand, `-x`; `pos` is the operator's.
export type Unary = { kind: 'unary'; op: string; operand: Expr; pos: Pos; bracketed?: true };

// An operator between two, `x + y`; `pos` is the operator's.
export type Binary = { kind: 'binary'; op: string; left: Expr; right: Expr; pos: Pos; bracketed?: true };

// `bracketed` says the expression was written in brackets of its own,
// `(x + y)`. The tree's shape already holds the grouping; this is for the
// places where perl gives the brackets themselves a meaning (a list
// against a scalar on the left of `=`, later).
export type Expr = Int | Unary | Binary;

export type Use = { kind: 'use'; version: string; pos: Pos };

// A builtin from the table of names, applied to its arguments.
export type Call = { kind: 'call'; name: string; args: readonly Expr[]; pos: Pos };

export type Stmt = Use | Call;

// `end` is where the file ends, for a diagnostic about what isn't there.
export type Program = { kind: 'program'; body: readonly Stmt[]; end: Pos };
