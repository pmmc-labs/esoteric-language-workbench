// The refusals that are rules of the language and not of its grammar
// (D29): a tree perl would accept and the language doesn't. It returns
// nothing; a tree that comes through is a program.
import { refuse } from './errors.ts';
import { BASED_MAX, DECIMAL_MAX_LENGTH, INT_MAX, PRAGMAS, VERSION, infixOp, prefixOp } from './names.ts';
import type { Call, Expr, Pragma, Program } from './ast.ts';

const checkExpr = (e: Expr): void => {
    if (e.kind === 'unary') return checkExpr(e.operand);
    if (e.kind === 'binary') {
        checkExpr(e.left);
        return checkExpr(e.right);
    }
    if (e.kind === 'apply') return e.args.forEach(checkExpr);
    // The lexer has seen to a string: its escapes, and its characters.
    if (e.kind === 'str') return;
    // perl reads `010` as octal, 8, doesn't compile `08`, and reads
    // `00.5` as two numbers joined (T24, T78). Octal is `0o10` (D38).
    if (/^0[0-9_]/.test(e.text)) {
        refuse(`${e.text} starts with a zero: perl reads that as octal, which the language writes 0o17`, e.pos);
    }
    if (e.kind === 'num') {
        // perl reads a decimal into a buffer of its own, and stops the
        // compile at 250 characters, underscores not counted (T91).
        if (e.text.replaceAll('_', '').length > DECIMAL_MAX_LENGTH) {
            refuse(`a number of more than ${DECIMAL_MAX_LENGTH} characters: perl refuses it as too long`, e.pos);
        }
        // perl makes it an infinity, in silence (T81); a Num is finite (D37).
        if (!Number.isFinite(e.value)) refuse(`${e.text} is past the largest float`, e.pos);
        return;
    }
    if (/^0[xXbBoO]/.test(e.text)) {
        if (e.value > BASED_MAX) refuse(`${e.text} is past 32 bits, where perl warns that a literal is not portable`, e.pos);
        return;
    }
    // perl carries on past here as an unsigned integer and then a float,
    // in silence (D23, T81). So -2^63 can't be written as a literal with
    // a minus: its digits are past the largest.
    if (e.value > INT_MAX) refuse(`${e.text} is past the largest integer, ${INT_MAX}`, e.pos);
};

// An expression behind any unary plus, which does nothing in perl either.
const plain = (e: Expr): Expr => (e.kind === 'unary' && prefixOp(e.op)?.rt === undefined ? plain(e.operand) : e);

// `say`'s argument is in list context, and there perl's `x` repeats a
// list when its left operand is in brackets: `say(("a") x 3)` is three
// values, not one string. They print the same, and cost perl a value
// each, so a count the string would bear stops perl for lack of memory
// (T101). Lists are step 9's: until then the brackets are refused.
const checkListContext = (call: Call): void => {
    const e = plain(call.args[0]!);
    if (e.kind === 'binary' && infixOp(e.op)?.list && plain(e.left).bracketed) {
        refuse(`(...) ${e.op} as ${call.name}'s argument repeats a list, to perl: take the brackets off the left operand`, e.pos);
    }
};

// A pragma is written one way (D16): its arguments are the table's, each
// a string literal. perl takes `use open qw(:std :encoding(UTF-8))` and
// `use open ':std', ':utf8'` too, and each is another thing to read.
const checkPragma = (p: Pragma): void => {
    const wanted = PRAGMAS.get(p.name)!.args;
    const written = p.args.map(a => (a.kind === 'str' && !a.bracketed ? a.value : undefined));
    if (written.length !== wanted.length || written.some((w, n) => w !== wanted[n])) {
        refuse(`'use ${p.name}' is written: use ${[p.name, wanted.map(a => `'${a}'`).join(', ')].join(' ').trim()};`, p.pos);
    }
};

export const check = (program: Program): void => {
    // The line that makes the file mean the same thing to perl (D16).
    const first = program.body[0];
    if (first === undefined || first.kind !== 'use' || first.version !== VERSION) {
        refuse(`a program begins 'use ${VERSION};'`, first?.pos ?? program.end);
    }
    // The pragmas come next, each once at most, before anything else.
    const seen = new Set<string>();
    let pragmas = true;
    for (const stmt of program.body.slice(1)) {
        if (stmt.kind === 'use') refuse(`'use ${stmt.version};' here: the version is the first statement, and is said once`, stmt.pos);
        else if (stmt.kind === 'pragma') {
            if (!pragmas) refuse(`'use ${stmt.name}' goes at the top, after 'use ${VERSION};' and before anything else`, stmt.pos);
            if (seen.has(stmt.name)) refuse(`'use ${stmt.name}' is said once`, stmt.pos);
            seen.add(stmt.name);
            checkPragma(stmt);
        } else {
            pragmas = false;
            stmt.args.forEach(checkExpr);
            checkListContext(stmt);
        }
    }
};
