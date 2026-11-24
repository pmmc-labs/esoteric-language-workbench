// The one table of names (D29): every word of the source that a pass acts
// on is here, with what the passes need to know of it, and no pass
// switches on a source string that isn't. It grows a row per feature. D21
// wants every name perl gives a meaning to in it, so that a program can't
// define a sub called `q`; that list comes with subs, at step 8.

export type Name =
    // `use VERSION;`, the only `use` so far (D16).
    | { kind: 'use' }
    // A builtin, written with brackets round its arguments or without
    // (D21). `args` is the shape of what follows it: `one`, a single
    // expression. `rt` is the runtime function the generated C calls.
    | { kind: 'builtin'; args: 'one'; rt: string };

export const NAMES: ReadonlyMap<string, Name> = new Map<string, Name>([
    ['use', { kind: 'use' }],
    ['say', { kind: 'builtin', args: 'one', rt: 'rt_say' }],
]);

// The perl whose meaning the language keeps (D2, D16).
export const VERSION = 'v5.42';

// The largest Int (D23): 2^63 - 1. A literal can't be negative: a minus
// before one is an operator, so the smallest Int, -2^63, has no literal.
export const INT_MAX = 9223372036854775807n;

// Operators: perlop's table, "Operator Precedence and Associativity", as
// perl 5.42's own perlop.pod has it, highest precedence first, every row
// of it though few are in the language yet. An operator with `in` is in;
// `rt` is the runtime function the generated C calls for it, and an
// operator that is in and has none does nothing (unary plus). The lexer
// takes the longest symbol here that matches, so `--` is never two minus
// signs and `**` never two stars, as perl has it (T27); the parser reads
// its precedence from a row's place in the list.
export type Assoc = 'left' | 'right' | 'nonassoc' | 'chained' | 'chain/na';
export type Op = { op: string; in?: true; rt?: string };
export type Level = {
    assoc: Assoc;
    prefix?: readonly Op[];     // before its operand
    infix?: readonly Op[];      // between two
    other?: readonly string[];  // neither: `++`, `?:`
    what?: string;              // perlop's words, for a row that isn't a list of symbols
};

const ops = (...names: string[]): Op[] => names.map(op => ({ op }));

export const PRECEDENCE: readonly Level[] = [
    { assoc: 'left', what: 'terms and list operators (leftward)' },
    { assoc: 'left', infix: ops('->') },
    { assoc: 'nonassoc', other: ['++', '--'] },
    { assoc: 'right', infix: ops('**') },
    { assoc: 'right', prefix: [...ops('!', '~', '~.', '\\'), { op: '+', in: true }, { op: '-', in: true, rt: 'rt_neg' }] },
    { assoc: 'left', infix: ops('=~', '!~') },
    { assoc: 'left', infix: [{ op: '*', in: true, rt: 'rt_mul' }, { op: '/' }, { op: '%', in: true, rt: 'rt_mod' }, { op: 'x' }] },
    { assoc: 'left', infix: [{ op: '+', in: true, rt: 'rt_add' }, { op: '-', in: true, rt: 'rt_sub' }, { op: '.' }] },
    { assoc: 'left', infix: ops('<<', '>>') },
    { assoc: 'nonassoc', what: 'named unary operators' },
    { assoc: 'nonassoc', infix: ops('isa') },
    { assoc: 'chained', infix: ops('<', '>', '<=', '>=', 'lt', 'gt', 'le', 'ge') },
    { assoc: 'chain/na', infix: ops('==', '!=', 'eq', 'ne', '<=>', 'cmp', '~~') },
    { assoc: 'left', infix: ops('&', '&.') },
    { assoc: 'left', infix: ops('|', '|.', '^', '^.') },
    { assoc: 'left', infix: ops('&&') },
    { assoc: 'left', infix: ops('||', '^^', '//') },
    { assoc: 'nonassoc', infix: ops('..', '...') },
    { assoc: 'right', other: ['?', ':'] },
    // "= += -= *= etc.": the list is perlop's, under Assignment Operators.
    { assoc: 'right', infix: ops('=', '**=', '+=', '*=', '&=', '&.=', '<<=', '&&=', '-=', '/=', '|=', '|.=', '>>=', '||=',
        '.=', '%=', '^=', '^.=', '//=', 'x=', '^^='), what: 'and goto last next redo dump' },
    { assoc: 'left', infix: ops(',', '=>') },
    { assoc: 'nonassoc', what: 'list operators (rightward)' },
    { assoc: 'right', prefix: ops('not') },
    { assoc: 'left', infix: ops('and') },
    { assoc: 'left', infix: ops('or', 'xor') },
];

// Every operator's spelling, the words among them too.
export const OPERATORS: ReadonlySet<string> = new Set(
    PRECEDENCE.flatMap(l => [...(l.prefix ?? []), ...(l.infix ?? [])].map(o => o.op).concat(l.other ?? [])));

// An operator in the language at this place, and its row; or undefined.
const find = (place: 'prefix' | 'infix') => (op: string): { row: number; assoc: Assoc; rt?: string } | undefined => {
    for (const [row, level] of PRECEDENCE.entries()) {
        const found = level[place]?.find(o => o.op === op && o.in);
        if (found) return { row, assoc: level.assoc, rt: found.rt };
    }
    return undefined;
};
export const prefixOp = find('prefix');
export const infixOp = find('infix');
