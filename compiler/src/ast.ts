// The syntax tree: the one data structure the passes share (D29). Plain
// objects with a `kind`, a position on every node, and nothing changed
// after the parser has made it. The vocabulary starts from Crayon's
// (docs/BACKGROUND.md), which had no positions and no record of brackets.

// Lines and columns count from 1, columns in code points.
export type Pos = { line: number; col: number };

// `text` is the literal as written, since `010` and `10` are different
// things to perl; `value` is what it is worth: `0x1F` and `1_000` too.
export type Int = { kind: 'int'; text: string; value: bigint; pos: Pos; bracketed?: true };

// A literal with a point or an exponent (D38). `value` is the double
// nearest to what it says, which is how perl reads one.
export type Num = { kind: 'num'; text: string; value: number; pos: Pos; bracketed?: true };

// A string literal (D24). `text` is the literal as written, quotes and
// all; `value` is the string, its characters as JavaScript holds them: a
// character past U+FFFF is two units there and one character here.
export type Str = { kind: 'str'; text: string; value: string; pos: Pos; bracketed?: true };

// An operator before its operand, `-x`; `pos` is the operator's.
export type Unary = { kind: 'unary'; op: string; operand: Expr; pos: Pos; bracketed?: true };

// An operator between two, `x + y`; `pos` is the operator's.
export type Binary = { kind: 'binary'; op: string; left: Expr; right: Expr; pos: Pos; bracketed?: true };

// `bracketed` says the expression was written in brackets of its own,
// `(x + y)`. The tree's shape already holds the grouping; this is for the
// places where perl gives the brackets themselves a meaning (a list
// against a scalar on the left of `=`, later).
export type Expr = Int | Num | Str | Unary | Binary | Apply;

// A builtin that has a value, applied to its arguments: `length "abc"`,
// `substr($s, 1)`. `pos` is the name's.
export type Apply = { kind: 'apply'; name: string; args: readonly Expr[]; pos: Pos; bracketed?: true };

export type Use = { kind: 'use'; version: string; pos: Pos };

// `use NAME ARGS;` (D16). Which names there are, and with which
// arguments, is the checker's to say, from the table.
export type Pragma = { kind: 'pragma'; name: string; args: readonly Expr[]; pos: Pos };

// A builtin that is a statement, `say` and `print`, and its arguments.
export type Call = { kind: 'call'; name: string; args: readonly Expr[]; pos: Pos };

export type Stmt = Use | Pragma | Call;

// `end` is where the file ends, for a diagnostic about what isn't there.
export type Program = { kind: 'program'; body: readonly Stmt[]; end: Pos };
