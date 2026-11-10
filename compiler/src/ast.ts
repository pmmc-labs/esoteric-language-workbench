// The shapes the parser builds and the interpreter reads. A position is kept
// only for syntax errors: a fault happens after parsing, so the tree has none.
export type Pos = { line: number; col: number };

export type Expr =
    | { kind: 'int'; value: bigint }
    | { kind: 'str'; value: string }
    | { kind: 'const'; name: 'nil' | 'true' | 'false' }
    | { kind: 'name'; name: string }
    | { kind: 'call'; fn: Expr; args: Expr[] }
    | { kind: 'method'; recv: Expr; name: string; args: Expr[] };

export type Stmt =
    | { kind: 'let'; name: string; expr: Expr }
    | { kind: 'expr'; expr: Expr };
