// The refusals that are rules of the language and not of its grammar
// (D29): a tree perl would accept and the language doesn't. It returns
// nothing; a tree that comes through is a program.
import { refuse } from './errors.ts';
import { INT_MAX, VERSION } from './names.ts';
import type { Expr, Program } from './ast.ts';

const checkExpr = (e: Expr): void => {
    // perl reads `010` as octal, 8, and doesn't compile `08` (T24).
    if (e.text.length > 1 && e.text[0] === '0') {
        refuse(`${e.text} starts with a zero, which perl reads as octal: not in the language yet`, e.pos);
    }
    // perl carries on past here as an unsigned integer and then a float
    // (D23); the language has neither kind of answer.
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
