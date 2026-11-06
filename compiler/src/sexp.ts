// The data the compiler works on. Every form carries where it came from.
export type Pos = { line: number; col: number };
export type Form =
    | { kind: 'int'; value: bigint; pos: Pos }
    | { kind: 'symbol'; name: string; pos: Pos }
    | { kind: 'list'; items: readonly Form[]; pos: Pos };

export const show = (f: Form): string =>
    f.kind === 'int' ? String(f.value)
    : f.kind === 'symbol' ? f.name
    : '(' + f.items.map(show).join(' ') + ')';
