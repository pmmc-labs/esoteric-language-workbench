// The refusals that are rules of the language and not of its grammar
// (D29): a tree perl would accept and the language doesn't. It returns
// nothing; a tree that comes through is a program.
import { refuse } from './errors.ts';
import { BASED_MAX, INT_MAX, VERSION } from './names.ts';
import type { Expr, Program } from './ast.ts';

const checkExpr = (e: Expr): void => {
    if (e.kind === 'unary') return checkExpr(e.operand);
    if (e.kind === 'binary') {
        checkExpr(e.left);
        return checkExpr(e.right);
    }
    // perl reads `010` as octal, 8, doesn't compile `08`, and reads
    // `00.5` as two numbers joined (T24, T78). Octal is `0o10` (D38).
    if (/^0[0-9_]/.test(e.text)) {
        refuse(`${e.text} starts with a zero: perl reads that as octal, which the language writes 0o17`, e.pos);
    }
    if (e.kind === 'num') {
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

export const check = (program: Program): void => {
    // The line that makes the file mean the same thing to perl (D16).
    const first = program.body[0];
    if (first === undefined || first.kind !== 'use' || first.version !== VERSION) {
        refuse(`a program begins 'use ${VERSION};'`, first?.pos ?? program.end);
    }
    for (const stmt of program.body.slice(1)) {
        if (stmt.kind === 'use') refuse(`'use ${stmt.version};' here: the only 'use' so far is the first statement`, stmt.pos);
        else stmt.args.forEach(checkExpr);
    }
};
