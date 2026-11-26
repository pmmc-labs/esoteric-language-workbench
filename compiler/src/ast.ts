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

// A double-quoted string with a variable in it (step 11a; D91 to D95):
// `parts` are its pieces from left to right, the text between as `str`s
// and each variable as the node it is outside a string (`var`, `array`,
// `elem`, `slice`, `lastindex`). It is one value, a Str, made where it
// stands (T196): no pass looks inside it for what a row of dots reads or
// a list names.
export type Interp = { kind: 'interp'; text: string; parts: readonly Expr[]; pos: Pos; bracketed?: true };

// An operator before its operand, `-x`; `pos` is the operator's.
export type Unary = { kind: 'unary'; op: string; operand: Expr; pos: Pos; bracketed?: true };

// An operator between two, `x + y`; `pos` is the operator's.
export type Binary = { kind: 'binary'; op: string; left: Expr; right: Expr; pos: Pos; bracketed?: true };

// `bracketed` says the expression was written in brackets of its own,
// `(x + y)`. The tree's shape already holds the grouping; this is for the
// places where perl gives the brackets themselves a meaning (a list
// against a scalar on the left of `=`, later).
export type Expr = Int | Num | Str | Interp | Constant | Var | My | Assign | Step | Unary | Binary | Ternary | Apply | Invoke
    | ArrayVar | MyArray | Elem | LastIndex | List | Slice | ArrayOp | ListAssign | ListOp | Binder | Sort | HashOp;

// An array, `@name`, and `my @name`, which declares one (D80).
// With `hash`, a hash, `%name` and `my %name` (step 12): the same nodes,
// because every rule about what an expression names, what is a list and
// the order things are worked out in is an array's (T218).
export type ArrayVar = { kind: 'array'; name: string; hash?: true; pos: Pos; bracketed?: true };
export type MyArray = { kind: 'myarray'; name: string; hash?: true; pos: Pos; bracketed?: true };

// An element, `$name[index]`, of the array `@name`; and `$#name`.
// With `hash`, `$name{key}`, of the hash `%name`, `index` its key.
export type Elem = { kind: 'elem'; name: string; index: Expr; hash?: true; pos: Pos; bracketed?: true };

// A builtin that names a hash (step 12a): `keys %name` and `values
// %name`; `exists $name{key}` and `delete $name{key}`; and `count`,
// `scalar(%name)` and `scalar` of its keys or values. `pos` is the
// word's, `at` the hash's.
// `delete @name{keys}` has `keys`, and gives a list (step 12b).
export type HashOp = { kind: 'hashop'; op: 'keys' | 'values' | 'exists' | 'delete' | 'count'; name: string; key?: Expr; keys?: readonly Expr[]; pos: Pos; at: Pos; bracketed?: true };
export type LastIndex = { kind: 'lastindex'; name: string; pos: Pos; bracketed?: true };

// A list in brackets: no items, or two and more, or one with a comma
// after it. (One item in brackets is that item, `bracketed`.) `my`: it
// followed the word, `my ($x, @rest)`, and declares what it names.
export type List = { kind: 'list'; items: readonly Expr[]; my?: true; pos: Pos; bracketed?: true };

// A slice: `@name[indexes]`, of an array, or `(items)[indexes]`, of a
// list. `pos` is the opening square bracket's.
// With `hash`, `@name{keys}`, of the hash `%name`, `indexes` its keys (step 12b).
export type Slice = { kind: 'slice'; name?: string; items?: readonly Expr[]; indexes: readonly Expr[]; hash?: true; pos: Pos; bracketed?: true };

// A builtin that names an array: `push @name, args`, `pop(@name)`,
// `splice(@name, args)`, `scalar(@name)`. `pos` is the word's, `at` the
// array's.
export type ArrayOp = { kind: 'arrayop'; op: string; name: string; args: readonly Expr[]; pos: Pos; at: Pos; bracketed?: true };

// `join(SEP, LIST)` and `reverse(LIST)`, with brackets or without (step
// 10a): the builtins that take a list and name no array.
export type ListOp = { kind: 'listop'; op: string; args: readonly Expr[]; pos: Pos; bracketed?: true };

// `map { ... } LIST` and `grep { ... } LIST` (step 10b): `body` is the
// block's statements, the last an expression, which is the block's value;
// `var` is `$_`, as a declaration, new for each value of the list.
export type Binder = { kind: 'binder'; op: string; var: My; body: readonly Stmt[]; items: readonly Expr[]; pos: Pos; bracketed?: true };

// `sort LIST` and `sort { ... } LIST` (step 10c). With a block: `a` and
// `b` are `$a` and `$b`, as declarations, new for each comparison, and
// `body` the block's statements, the last an expression, which says
// which of the two comes first.
export type Sort = { kind: 'sort'; a?: My; b?: My; body?: readonly Stmt[]; items: readonly Expr[]; pos: Pos; bracketed?: true };

// A list assignment, `(targets) = value` and `my (targets) = value`: a
// statement (D78). A target is a variable, an element, `undef`, or, last,
// an array.
export type ListAssign = { kind: 'listassign'; targets: readonly Expr[]; my?: true; value: Expr; pos: Pos; bracketed?: true };

// A variable, `$name`; and `my $name`, which declares one where it stands
// and is that variable (D56). Which declaration a `Var` means is the
// resolver's to say.
export type Var = { kind: 'var'; name: string; pos: Pos; bracketed?: true };
export type My = { kind: 'my'; name: string; pos: Pos; bracketed?: true };

// `$x = E`, `$x += E`: `pos` is the operator's. Its value is the variable.
export type Assign = { kind: 'assign'; op: string; target: Var | My | Elem | ArrayVar | MyArray; value: Expr; pos: Pos; bracketed?: true };

// `++$x`, `$x++`, `--$x`, `$x--`: `before` says the operator comes first.
export type Step = { kind: 'step'; op: string; before: boolean; target: Var | Elem; pos: Pos; bracketed?: true };

// A word that is a value: `true`, `false`, `undef` (D47, D48).
export type Constant = { kind: 'constant'; name: string; pos: Pos; bracketed?: true };

// `test ? then : else`; `pos` is the question mark's.
export type Ternary = { kind: 'ternary'; test: Expr; then: Expr; else: Expr; pos: Pos; bracketed?: true };

// A builtin that has a value, applied to its arguments: `length "abc"`,
// `substr($s, 1)`. `pos` is the name's.
export type Apply = { kind: 'apply'; name: string; args: readonly Expr[]; pos: Pos; bracketed?: true };

// A call of one of the program's own subs, `name(args)` (D21, D72). `pos`
// is the name's.
export type Invoke = { kind: 'invoke'; name: string; args: readonly Expr[]; pos: Pos; bracketed?: true };

export type Use = { kind: 'use'; version: string; pos: Pos };

// `use NAME ARGS;` (D16). Which names there are, and with which
// arguments, is the checker's to say, from the table.
// (`no warnings ...;` is the pragma named `no warnings`, D67.)
export type Pragma = { kind: 'pragma'; name: string; args: readonly Expr[]; pos: Pos };

// A builtin that is a statement, `say` and `print`, and its arguments.
export type Call = { kind: 'call'; name: string; args: readonly Expr[]; pos: Pos };

// An expression as a statement: an assignment, a `++` or `--`, a `my`.
export type Do = { kind: 'do'; expr: Expr; pos: Pos };

// `{ ... }`: a scope.
export type Block = { kind: 'block'; body: readonly Stmt[]; pos: Pos };

// `if (T) { } elsif (T) { } else { }`, one arm a test. `unless` is one arm
// with `negate`; `STATEMENT if T;` is one arm with `modifier`, its body
// the statement.
export type Arm = { test: Expr; negate?: true; body: readonly Stmt[]; pos: Pos };
export type If = { kind: 'if'; arms: readonly Arm[]; otherwise?: readonly Stmt[]; modifier?: true; pos: Pos };

// A loop's label, `NAME:` (D61).
export type Label = { name: string; pos: Pos };

// `while (T) { }`, and `until` with `negate`; `STATEMENT while T;` with
// `modifier`, its body the statement, which tests first all the same.
export type While = { kind: 'while'; test: Expr; negate?: true; body: readonly Stmt[]; label?: Label; modifier?: true; pos: Pos };

// `for (FIRST; TEST; EACH) { }`: FIRST and EACH are expressions with
// commas between them (D60), and no TEST is true.
export type For = { kind: 'for'; first: readonly Expr[]; test?: Expr; each: readonly Expr[]; body: readonly Stmt[]; label?: Label; pos: Pos };

// `for my $x (LIST) { }`, and spelled `foreach` (D17, D77, D80): the
// block once for each value of the list, `var` a copy of it and new each
// time round.
// `for (LIST) { }` is the same with `$_` for its variable, and `STATEMENT
// for LIST;` that with `modifier`, its body the statement (step 10b).
export type Foreach = { kind: 'foreach'; var: My; items: readonly Expr[]; body: readonly Stmt[]; label?: Label; modifier?: true; pos: Pos };

// `last;` and `next;`, with a label or without (D62). `name` is the word.
export type Jump = { kind: 'jump'; name: string; label?: Label; pos: Pos };

// A parameter of a sub (D72): `$name`, or `$` alone, which takes an
// argument and names nothing; and its default, if it has one, with the
// operator it was written with: `=`, `//=` or `||=`. `my` is the variable
// as a declaration, for the resolver. `pos` is the `$`'s.
// A slurpy parameter, `@name` or `@` alone, the last: `slurpy`, and `rest`
// its array as a declaration if it has a name.
// With `hash`, `%name` or `%` alone: what is left, as keys and values.
export type Param = { my?: My; op?: string; default?: Expr; slurpy?: true; hash?: true; rest?: MyArray; pos: Pos };

// `sub name(params) { body }`. `pos` is the word `sub`'s, `named` the
// name's, and `end` the closing brace's.
export type Sub = { kind: 'sub'; name: string; params: readonly Param[]; body: readonly Stmt[]; pos: Pos; named: Pos; end: Pos };

// `return;` and `return value;`.
export type Return = { kind: 'return'; value?: Expr; pos: Pos };

export type Loop = While | For | Foreach;
export type Stmt = Use | Pragma | Call | Do | Block | If | While | For | Foreach | Jump | Sub | Return;

// `end` is where the file ends, for a diagnostic about what isn't there.
export type Program = { kind: 'program'; body: readonly Stmt[]; end: Pos };
