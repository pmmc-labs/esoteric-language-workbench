// The one table of names (D29): every word of the source that a pass acts
// on is here, with what the passes need to know of it, and no pass
// switches on a source string that isn't. It grows a row per feature. D21
// wants every name perl gives a meaning to in it, so that a program can't
// define a sub called `q`: that list is PERL_WORDS, below.

export type Name =
    // `use VERSION;` and `use PRAGMA ...;` (D16).
    | { kind: 'use' }
    // A builtin that is a statement: `say EXPR;`, with brackets round its
    // one argument or without (D21). `rt` is the runtime function the
    // generated C calls.
    | { kind: 'statement'; rt: string }
    // One of perl's named unary operators (D41): one argument, in brackets
    // or without, and without them it takes everything that binds tighter
    // than the row of perlop's table that is theirs.
    | { kind: 'unary'; rt: string }
    // A word that is a value (D47, D48). `c` is the C for it. `bare`: perl
    // takes what follows the word for its argument whenever it can, so
    // only what can't be one may follow it (`undef`, T105).
    | { kind: 'constant'; c: string; bare?: true }
    // The words of step 5's statements (D56). `unless` is an `if` whose
    // test is turned round, and takes no `elsif` or `else` (D54).
    | { kind: 'my' }
    | { kind: 'if'; unless?: true }
    | { kind: 'elsif' }
    | { kind: 'else' }
    // The words of step 6's (D62). `until` is a `while` whose test is
    // turned round; both are modifiers too. `for` is the C-style loop, and the
    // loop over a list, which is all `foreach` is here (step 9b).
    // `last` leaves its loop, and `next` goes on to its next time round.
    | { kind: 'while'; until?: true }
    | { kind: 'for'; each?: true }
    | { kind: 'jump'; leaves?: true }
    // The words of step 8's (D72): `sub NAME(...) { }`, `return`, and
    // `no`, which begins the one pragma that is turned off (D67).
    | { kind: 'sub' }
    | { kind: 'return' }
    | { kind: 'no' }
    // The builtins that name an array (D80): `push` and `unshift` take the
    // array and a list, with brackets or without; `pop` and `shift` the
    // array, in brackets unless it ends the expression (T152); `splice`
    // and `scalar` always have brackets.
    | { kind: 'arrayop'; shape: 'push' | 'pop' | 'splice' | 'scalar'; rt: string }
    // The builtins that take a list and name no array (step 10a): `join`,
    // a separator and a list, and `reverse`, a list; with brackets or
    // without.
    | { kind: 'listop'; rt: string }
    // `map` and `grep` (step 10b): a block and a list, and no brackets of
    // their own (D85, D87).
    | { kind: 'binder' }
    // `sort` (step 10c): a list, or a block and a list.
    | { kind: 'sort' }
    // The builtins that name a hash (step 12a): `keys` and `values` take
    // the hash, `exists` and `delete` an element of one; with brackets or
    // without, and without them nothing that binds tighter than a named
    // unary operator may follow (T220, T225).
    | { kind: 'hashop'; shape: 'hash' | 'elem' }
    // A builtin whose arguments are in brackets, always (D41): `min` to
    // `min + rt.length - 1` of them, each count with a runtime function
    // of its own.
    | { kind: 'function'; min: number; rt: readonly string[] };

export const NAMES: ReadonlyMap<string, Name> = new Map<string, Name>([
    ['use', { kind: 'use' }],
    ['say', { kind: 'statement', rt: 'rt_say_list' }],
    ['print', { kind: 'statement', rt: 'rt_print_list' }],
    // Step 16b (D128): `printf` is a statement as `print` is, and
    // `sprintf` a value as `join` is; the list's first value is the
    // format, which compiler/src/format.ts reads.
    ['printf', { kind: 'statement', rt: 'rt_printf' }],
    ['length', { kind: 'unary', rt: 'rt_length' }],
    ['uc', { kind: 'unary', rt: 'rt_uc' }],
    ['lc', { kind: 'unary', rt: 'rt_lc' }],
    ['ord', { kind: 'unary', rt: 'rt_ord' }],
    ['chr', { kind: 'unary', rt: 'rt_chr' }],
    ['defined', { kind: 'unary', rt: 'rt_defined' }],
    ['true', { kind: 'constant', c: 'rt_bool(1)' }],
    ['false', { kind: 'constant', c: 'rt_bool(0)' }],
    ['undef', { kind: 'constant', c: 'rt_undef()', bare: true }],
    ['my', { kind: 'my' }],
    ['if', { kind: 'if' }],
    ['unless', { kind: 'if', unless: true }],
    ['elsif', { kind: 'elsif' }],
    ['else', { kind: 'else' }],
    ['while', { kind: 'while' }],
    ['until', { kind: 'while', until: true }],
    ['for', { kind: 'for' }],
    ['foreach', { kind: 'for', each: true }],
    ['last', { kind: 'jump', leaves: true }],
    ['next', { kind: 'jump' }],
    ['sub', { kind: 'sub' }],
    ['return', { kind: 'return' }],
    ['no', { kind: 'no' }],
    ['push', { kind: 'arrayop', shape: 'push', rt: 'rt_push' }],
    ['unshift', { kind: 'arrayop', shape: 'push', rt: 'rt_unshift' }],
    ['pop', { kind: 'arrayop', shape: 'pop', rt: 'rt_pop' }],
    ['shift', { kind: 'arrayop', shape: 'pop', rt: 'rt_shift' }],
    ['splice', { kind: 'arrayop', shape: 'splice', rt: 'rt_splice' }],
    ['scalar', { kind: 'arrayop', shape: 'scalar', rt: 'rt_count' }],
    ['join', { kind: 'listop', rt: 'rt_join' }],
    ['sprintf', { kind: 'listop', rt: 'rt_sprintf' }],
    ['map', { kind: 'binder' }],
    ['grep', { kind: 'binder' }],
    ['sort', { kind: 'sort' }],
    ['reverse', { kind: 'listop', rt: 'rt_list_add_reversed' }],
    ['keys', { kind: 'hashop', shape: 'hash' }],
    ['values', { kind: 'hashop', shape: 'hash' }],
    ['exists', { kind: 'hashop', shape: 'elem' }],
    ['delete', { kind: 'hashop', shape: 'elem' }],
    ['substr', { kind: 'function', min: 2, rt: ['rt_substr2', 'rt_substr3'] }],
    ['index', { kind: 'function', min: 2, rt: ['rt_index2', 'rt_index3'] }],
]);

// Every word perl 5.42 gives a meaning to: its own keyword table, whole
// (regen/keywords.pl of the 5.42.0 source, 266 words), whether the
// language has the word or not. A program may not name a sub for one
// (D21): perl would ignore the definition, or not compile the call (T28).
export const PERL_KEYWORDS: readonly string[] = [
    'ADJUST', 'AUTOLOAD', 'BEGIN', 'CHECK', 'DESTROY', 'END', 'INIT',
    'UNITCHECK', '__CLASS__', '__DATA__', '__END__', '__FILE__', '__LINE__',
    '__PACKAGE__', '__SUB__', 'abs', 'accept', 'alarm', 'all', 'and', 'any',
    'atan2', 'bind', 'binmode', 'bless', 'break', 'caller', 'catch', 'chdir',
    'chmod', 'chomp', 'chop', 'chown', 'chr', 'chroot', 'class', 'close',
    'closedir', 'cmp', 'connect', 'continue', 'cos', 'crypt', 'dbmclose',
    'dbmopen', 'default', 'defer', 'defined', 'delete', 'die', 'do', 'dump',
    'each', 'else', 'elsif', 'endgrent', 'endhostent', 'endnetent',
    'endprotoent', 'endpwent', 'endservent', 'eof', 'eq', 'eval', 'evalbytes',
    'exec', 'exists', 'exit', 'exp', 'fc', 'fcntl', 'field', 'fileno',
    'finally', 'flock', 'for', 'foreach', 'fork', 'format', 'formline', 'ge',
    'getc', 'getgrent', 'getgrgid', 'getgrnam', 'gethostbyaddr',
    'gethostbyname', 'gethostent', 'getlogin', 'getnetbyaddr', 'getnetbyname',
    'getnetent', 'getpeername', 'getpgrp', 'getppid', 'getpriority',
    'getprotobyname', 'getprotobynumber', 'getprotoent', 'getpwent',
    'getpwnam', 'getpwuid', 'getservbyname', 'getservbyport', 'getservent',
    'getsockname', 'getsockopt', 'given', 'glob', 'gmtime', 'goto', 'grep',
    'gt', 'hex', 'if', 'index', 'int', 'ioctl', 'isa', 'join', 'keys', 'kill',
    'last', 'lc', 'lcfirst', 'le', 'length', 'link', 'listen', 'local',
    'localtime', 'lock', 'log', 'lstat', 'lt', 'm', 'map', 'method', 'mkdir',
    'msgctl', 'msgget', 'msgrcv', 'msgsnd', 'my', 'ne', 'next', 'no', 'not',
    'oct', 'open', 'opendir', 'or', 'ord', 'our', 'pack', 'package', 'pipe',
    'pop', 'pos', 'print', 'printf', 'prototype', 'push', 'q', 'qq', 'qr',
    'quotemeta', 'qw', 'qx', 'rand', 'read', 'readdir', 'readline',
    'readlink', 'readpipe', 'recv', 'redo', 'ref', 'rename', 'require',
    'reset', 'return', 'reverse', 'rewinddir', 'rindex', 'rmdir', 's', 'say',
    'scalar', 'seek', 'seekdir', 'select', 'semctl', 'semget', 'semop',
    'send', 'setgrent', 'sethostent', 'setnetent', 'setpgrp', 'setpriority',
    'setprotoent', 'setpwent', 'setservent', 'setsockopt', 'shift', 'shmctl',
    'shmget', 'shmread', 'shmwrite', 'shutdown', 'sin', 'sleep', 'socket',
    'socketpair', 'sort', 'splice', 'split', 'sprintf', 'sqrt', 'srand',
    'stat', 'state', 'study', 'sub', 'substr', 'symlink', 'syscall',
    'sysopen', 'sysread', 'sysseek', 'system', 'syswrite', 'tell', 'telldir',
    'tie', 'tied', 'time', 'times', 'tr', 'truncate', 'try', 'uc', 'ucfirst',
    'umask', 'undef', 'unless', 'unlink', 'unpack', 'unshift', 'untie',
    'until', 'use', 'utime', 'values', 'vec', 'wait', 'waitpid', 'wantarray',
    'warn', 'when', 'while', 'write', 'x', 'xor', 'y',
];

// And the names that are not keywords and are not free either: the
// functions `use v5.42;` brings in from `builtin` (perl warns of a sub
// named for one, T28), with the rest of that module's; the subs perl
// calls by itself; and its file handles, which it would rather read after
// `say` than call.
export const PERL_OTHER: readonly string[] = [
    'true', 'false', 'inf', 'nan', 'weaken', 'unweaken', 'is_weak', 'blessed', 'refaddr', 'reftype', 'ceil', 'floor',
    'is_tainted', 'trim', 'stringify', 'created_as_string', 'created_as_number', 'indexed', 'is_bool', 'export_lexically',
    'load_module',
    'import', 'unimport', 'CLONE', 'CLONE_SKIP',
    'STDIN', 'STDOUT', 'STDERR', 'ARGV', 'ARGVOUT', 'DATA', 'ENV', 'INC',
];

export const PERL_WORDS: ReadonlySet<string> = new Set([...PERL_KEYWORDS, ...PERL_OTHER]);

// `v`, a digit, and digits or underscores: a version string to perl when
// it has not yet seen a sub of that name (T136).
export const isVersionString = (word: string): boolean => /^v[0-9][0-9_]*$/.test(word);

// The perl whose meaning the language keeps (D2, D16).
export const VERSION = 'v5.42';

// The pragmas, a closed list (D16): each with the arguments it must be
// written with, as strings. `rt` is what one does when the program starts,
// if anything; `utf8` is the lexer's business and nothing else's.
export type Pragma = { args: readonly string[]; rt?: string };
export const PRAGMAS: ReadonlyMap<string, Pragma> = new Map<string, Pragma>([
    ['utf8', { args: [] }],
    // Written `no warnings 'recursion';` (D67): it changes nothing here,
    // and under perl it silences the warning at 100 calls deep. The key is
    // the two words, since `use warnings` is no pragma of the language's.
    ['no warnings', { args: ['recursion'] }],
    // perl's standard streams as UTF-8 (D39).
    ['open', { args: [':std', ':encoding(UTF-8)'], rt: 'rt_use_open' }],
]);

// The largest Unicode scalar value, and the surrogates, which aren't any
// (D42).
export const isScalarValue = (n: number): boolean => n >= 0 && n <= 0x10FFFF && !(n >= 0xD800 && n <= 0xDFFF);
// The 66 noncharacters: perl warns when one is printed (T88).
export const isNoncharacter = (n: number): boolean => (n >= 0xFDD0 && n <= 0xFDEF) || (n & 0xFFFE) === 0xFFFE;

// The largest Int (D23): 2^63 - 1. A literal can't be negative: a minus
// before one is an operator, so the smallest Int, -2^63, has no literal.
export const INT_MAX = 9223372036854775807n;

// The largest hex, binary or octal literal (D38): perl warns that a
// larger one is not portable.
export const BASED_MAX = 0xFFFFFFFFn;

// The longest decimal literal perl compiles, in characters, underscores
// aside: one more is `Number too long` (T91).
export const DECIMAL_MAX_LENGTH = 250;

// Operators: perlop's table, "Operator Precedence and Associativity", as
// perl 5.42's own perlop.pod has it, highest precedence first, every row
// of it though few are in the language yet. An operator with `in` is in;
// `rt` is the runtime function the generated C calls for it, and an
// operator that is in and has none does nothing (unary plus). The lexer
// takes the longest symbol here that matches, so `--` is never two minus
// signs and `**` never two stars, as perl has it (T27); the parser reads
// its precedence from a row's place in the list.
export type Assoc = 'left' | 'right' | 'nonassoc' | 'chained' | 'chain/na';
// `list`: in list context, with its left operand in brackets, the
// operator works on a list (`x`). `sign`: a prefix operator perl warns
// about after a named unary operator (T94). `when`: the operator works its
// right operand out only when this runtime test says so of its left, and
// its value is one operand or the other (D49). `logic`: it takes an undef,
// and may follow a bare `undef` (D48). `bang`: perl warns of a precedence
// problem when the operator, unbracketed, is the left operand of a
// comparison (T115). `assign`: the operator puts a value in the variable
// on its left: what `rt` gives of the variable and the right side, or the
// right side itself if there is no `rt`, and with `when` only when the
// test says so of the variable (D56). `concat`: perl joins a row of these
// as one operation (D57). `tests`: a prefix operator that tests its
// operand for truth, and hands a test on to it (D53).
export type Op = { op: string; in?: true; rt?: string; range?: true; list?: true; sign?: true; when?: string; logic?: true; bang?: true; assign?: true; concat?: true; tests?: true };
export type Level = {
    assoc: Assoc;
    prefix?: readonly Op[];     // before its operand
    infix?: readonly Op[];      // between two
    other?: readonly string[];  // neither: `++`, `?:`
    what?: string;              // perlop's words, for a row that isn't a list of symbols
};

const ops = (...names: string[]): Op[] => names.map(op => ({ op }));
const live = (op: string, rt: string): Op => ({ op, in: true, rt });
const lazy = (op: string, when: string): Op => ({ op, in: true, when, logic: true });
const put = (op: string, rt: string): Op => ({ op, in: true, rt, assign: true });
const NAMED_UNARY = 'named unary operators';

export const PRECEDENCE: readonly Level[] = [
    { assoc: 'left', what: 'terms and list operators (leftward)' },
    { assoc: 'left', infix: ops('->') },
    { assoc: 'nonassoc', other: ['++', '--'] },
    { assoc: 'right', infix: [{ op: '**', in: true, rt: 'rt_pow' }] },
    { assoc: 'right', prefix: [{ op: '!', in: true, rt: 'rt_not', bang: true, tests: true }, ...ops('~', '~.', '\\'), { op: '+', in: true, sign: true }, { op: '-', in: true, rt: 'rt_neg', sign: true }] },
    { assoc: 'left', infix: ops('=~', '!~') },
    { assoc: 'left', infix: [{ op: '*', in: true, rt: 'rt_mul' }, { op: '/', in: true, rt: 'rt_div' }, { op: '%', in: true, rt: 'rt_mod' }, { op: 'x', in: true, rt: 'rt_repeat', list: true }] },
    { assoc: 'left', infix: [{ op: '+', in: true, rt: 'rt_add' }, { op: '-', in: true, rt: 'rt_sub' }, { op: '.', in: true, rt: 'rt_concat', concat: true }] },
    { assoc: 'left', infix: ops('<<', '>>') },
    { assoc: 'nonassoc', what: NAMED_UNARY },
    { assoc: 'nonassoc', infix: ops('isa') },
    { assoc: 'chained', infix: [live('<', 'rt_num_lt'), live('>', 'rt_num_gt'), live('<=', 'rt_num_le'), live('>=', 'rt_num_ge'),
        live('lt', 'rt_str_lt'), live('gt', 'rt_str_gt'), live('le', 'rt_str_le'), live('ge', 'rt_str_ge')] },
    { assoc: 'chain/na', infix: [live('==', 'rt_num_eq'), live('!=', 'rt_num_ne'), live('eq', 'rt_str_eq'), live('ne', 'rt_str_ne'),
        live('<=>', 'rt_num_cmp'), live('cmp', 'rt_str_cmp'), ...ops('~~')] },
    { assoc: 'left', infix: ops('&', '&.') },
    { assoc: 'left', infix: ops('|', '|.', '^', '^.') },
    { assoc: 'left', infix: [lazy('&&', 'rt_is_true')] },
    { assoc: 'left', infix: [lazy('||', 'rt_is_false'), ...ops('^^'), lazy('//', 'rt_is_undef')] },
    // A range, in a list (D80): whole numbers from one end to the other.
    { assoc: 'nonassoc', infix: [{ op: '..', in: true, range: true }, ...ops('...')] },
    { assoc: 'right', other: ['?', ':'] },
    // "= += -= *= etc.": the list is perlop's, under Assignment Operators.
    // An undef on the left of `+=`, `-=` and `.=` is 0 or the empty
    // string, as perl has it, and those three have functions of their own.
    { assoc: 'right', infix: [{ op: '=', in: true, assign: true }, put('**=', 'rt_pow'), put('+=', 'rt_add_to'), put('*=', 'rt_mul'),
        put('-=', 'rt_sub_from'), put('/=', 'rt_div'), { ...put('.=', 'rt_concat_to'), concat: true }, put('%=', 'rt_mod'), put('x=', 'rt_repeat'),
        { op: '&&=', in: true, assign: true, when: 'rt_is_true' }, { op: '||=', in: true, assign: true, when: 'rt_is_false' },
        { op: '//=', in: true, assign: true, when: 'rt_is_undef' },
        ...ops('&=', '&.=', '<<=', '|=', '|.=', '>>=', '^=', '^.=', '^^=')], what: 'and goto last next redo dump' },
    { assoc: 'left', infix: ops(',', '=>') },
    { assoc: 'nonassoc', what: 'list operators (rightward)' },
    { assoc: 'right', prefix: [{ ...live('not', 'rt_not'), tests: true }] },
    { assoc: 'left', infix: [lazy('and', 'rt_is_true')] },
    { assoc: 'left', infix: [lazy('or', 'rt_is_false'), { op: 'xor', in: true, rt: 'rt_xor', logic: true }] },
];

// Every operator's spelling, the words among them too.
export const OPERATORS: ReadonlySet<string> = new Set(
    PRECEDENCE.flatMap(l => [...(l.prefix ?? []), ...(l.infix ?? [])].map(o => o.op).concat(l.other ?? [])));

// An operator in the language at this place, and its row; or undefined.
export type Found = { row: number; assoc: Assoc } & Omit<Op, 'op' | 'in'>;
const find = (place: 'prefix' | 'infix') => (op: string): Found | undefined => {
    for (const [row, level] of PRECEDENCE.entries()) {
        const found = level[place]?.find(o => o.op === op && o.in);
        if (found) return { ...found, row, assoc: level.assoc };
    }
    return undefined;
};
export const prefixOp = find('prefix');
export const infixOp = find('infix');

// `++` and `--`, which stand before a variable or after it (D52). `rt`
// gives what the variable holds afterwards, and `before` what `$x++` is
// worth when that isn't simply what `$x` held (an undef is 0, T43).
export type StepOp = { rt: string; before?: string };
const STEPS: ReadonlyMap<string, StepOp> = new Map([['++', { rt: 'rt_inc', before: 'rt_before_inc' }], ['--', { rt: 'rt_dec' }]]);
export const stepOp = (op: string): StepOp | undefined => STEPS.get(op);

// The names a variable may not have (D55): perl's `sort` owns `$a` and
// `$b`, and `$_` is its own thing.
// A label: capitals, digits and `_`, a capital first (D61).
export const isLabel = (word: string): boolean => /^[A-Z][A-Z0-9_]*$/.test(word);

// The longest name perl takes: one more is `Identifier too long` (T126).
export const NAME_MAX_LENGTH = 251;

export const RESERVED: ReadonlySet<string> = new Set(['a', 'b', '_']);

// The row of the named unary operators: `length`, written without
// brackets, takes for its argument everything in the rows above this one.
export const NAMED_UNARY_ROW = PRECEDENCE.findIndex(l => l.what === NAMED_UNARY);

// The row of `? :`, which is neither before nor between; of the comma,
// which a list of arguments is made of; and of `and`, the tightest of the
// word operators that stand between two operands.
export const TERNARY_ROW = PRECEDENCE.findIndex(l => l.other?.includes('?'));
export const COMMA_ROW = PRECEDENCE.findIndex(l => l.infix?.some(o => o.op === ','));
export const AND_ROW = PRECEDENCE.findIndex(l => l.infix?.some(o => o.op === 'and'));
