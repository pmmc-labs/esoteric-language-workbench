// The one table of names (D29): every word of the source that a pass acts
// on is here, with what the passes need to know of it, and no pass
// switches on a source string that isn't. It grows a row per feature. D21
// wants every name perl gives a meaning to in it, so that a program can't
// define a sub called `q`; that list comes with subs, at step 8.

export type Name =
    // `use VERSION;`, the only `use` so far (D16).
    | { kind: 'use' }
    // A builtin written without brackets. `args` is the shape of what
    // follows it, `rt` the runtime function the generated C calls.
    | { kind: 'builtin'; args: 'int'; rt: string };

export const NAMES: ReadonlyMap<string, Name> = new Map<string, Name>([
    ['use', { kind: 'use' }],
    ['say', { kind: 'builtin', args: 'int', rt: 'rt_say' }],
]);

// The perl whose meaning the language keeps (D2, D16).
export const VERSION = 'v5.42';

// The largest Int (D23): 2^63 - 1. A literal can't be negative; step 1's
// unary minus makes the negative ones.
export const INT_MAX = 9223372036854775807n;
