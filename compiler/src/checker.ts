// The refusals that are rules of the language and not of its grammar
// (D29): a tree perl would accept and the language doesn't. It returns
// nothing; a tree that comes through is a program.
import { refuse } from './errors.ts';
import { BASED_MAX, DECIMAL_MAX_LENGTH, INT_MAX, PRAGMAS, VERSION, infixOp, prefixOp } from './names.ts';
import type { Call, Expr, Pragma, Program, Stmt } from './ast.ts';

// The expressions an expression is made of, in the order they are worked
// out.
const parts = (e: Expr): readonly Expr[] =>
    e.kind === 'unary' ? [e.operand]
    : e.kind === 'binary' ? [e.left, e.right]
    : e.kind === 'ternary' ? [e.test, e.then, e.else]
    : e.kind === 'apply' ? e.args
    : e.kind === 'assign' ? [e.value, e.target]
    : e.kind === 'step' ? [e.target]
    : [];

const checkLiteral = (e: Expr): void => {
    if (e.kind !== 'int' && e.kind !== 'num') return;
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

// Whether a variable is anywhere in an expression.
const hasVariable = (e: Expr): boolean => e.kind === 'var' || e.kind === 'my' || parts(e).some(hasVariable);

// The names an expression reads, and the ones it changes: by name, which
// is a little more than by declaration, and errs toward refusing.
const reads = (e: Expr, into = new Set<string>()): Set<string> => {
    if (e.kind === 'var' || e.kind === 'my') into.add(e.name);
    parts(e).forEach(p => reads(p, into));
    return into;
};
const changes = (e: Expr, into = new Set<string>()): Set<string> => {
    if (e.kind === 'assign' || e.kind === 'step') into.add(e.target.name);
    parts(e).forEach(p => changes(p, into));
    return into;
};

// perl joins a row of dots as one operation, and reads every piece when
// it runs: `$x . "a" . ($x = 5)` is `5a5`, where the first dot alone
// would have made `3a` (T117). How far a row reaches turns on what perl
// folds away as it compiles (`(1 ? $x . "a" : 0) . ($x = 5)` is a row
// too), and on its length. So a later piece of a concatenation may not
// change a variable an earlier piece reads (D57); a piece is found
// through brackets, a unary plus, and both sides of whatever gives one
// operand or the other.
const pieces = (e: Expr): Expr[] => {
    const p = plain(e);
    if (p.kind === 'binary' && (infixOp(p.op)?.concat || infixOp(p.op)?.when)) return [...pieces(p.left), ...pieces(p.right)];
    if (p.kind === 'ternary') return [p.test, ...pieces(p.then), ...pieces(p.else)];
    return [p];
};
const checkConcat = (e: Expr): void => {
    const row = e.kind === 'binary' && infixOp(e.op)?.concat ? pieces(e)
        : e.kind === 'assign' && infixOp(e.op)?.concat ? [e.target, ...pieces(e.value)]
        : [];
    const read = new Set<string>();
    for (const piece of row) {
        for (const name of changes(piece)) {
            if (read.has(name)) {
                refuse(`a later piece of a concatenation changes $${name}, which an earlier piece reads: perl joins the pieces as one operation and reads each late; make the change a statement of its own`, piece.pos);
            }
        }
        reads(piece, read);
    }
};

// A `=` whose right side has no variable in it, where its value is tested
// for truth: `if ($x = 5)` (D53). perl warns `Found = in conditional`
// when the right side is a constant, after folding what it can (T112);
// this is that and a little more, with no folder. `tested` goes down
// through what hands a test on: a unary plus, `!` and `not` (perl takes
// the `!` of a condition away and tests the other way), the right of an
// operator that gives one operand or the other, and the branches of `? :`.
const tested = (in_: Expr): void => {
    const e = plain(in_);
    if (e.kind === 'unary' && prefixOp(e.op)?.tests) return tested(e.operand);
    if (e.kind === 'assign' && infixOp(e.op)?.rt === undefined && infixOp(e.op)?.when === undefined && !hasVariable(e.value)) {
        refuse(`'${e.op}' where a value is tested, with nothing but a constant on its right: perl warns that == was meant`, e.pos);
    }
    // Both operands: under a `!`, perl has the left one tested too.
    if (e.kind === 'binary' && infixOp(e.op)?.when) {
        tested(e.left);
        tested(e.right);
    }
    if (e.kind === 'ternary') {
        tested(e.then);
        tested(e.else);
    }
};

// Everything that is checked of an expression wherever it stands.
// `my`: whether a `my` may stand here (D56, D21): at the head of a
// statement, or in the test of an `if`, and in neither under an operand
// that may not be worked out.
const checkExpr = (e: Expr, my: boolean): void => {
    checkLiteral(e);
    checkConcat(e);
    if (e.kind === 'my' && !my) {
        refuse(`my $${e.name} here: a my begins a statement, or stands in the test of an if, where it is always reached`, e.pos);
    }
    if (e.kind === 'ternary') {
        tested(e.test);
        checkExpr(e.test, my);
        checkExpr(e.then, false);
        return checkExpr(e.else, false);
    }
    if (e.kind === 'binary' && infixOp(e.op)?.when) {
        tested(e.left);
        checkExpr(e.left, my);
        return checkExpr(e.right, false);
    }
    if (e.kind === 'assign' && infixOp(e.op)?.when) {
        checkExpr(e.target, my);
        return checkExpr(e.value, false);
    }
    parts(e).forEach(p => checkExpr(p, my));
};

// `say`'s argument is in list context, and there perl's `x` repeats a
// list when its left operand is in brackets: `say(("a") x 3)` is three
// values, not one string. They print the same, and cost perl a value
// each, so a count the string would bear stops perl for lack of memory
// (T101). Lists are step 9's: until then the brackets are refused.
//
// The list reaches down: to the right operand of an operator that gives
// one operand or the other (`||`, `&&`, `//`, `or`, `and`), and to both
// branches of `? :` (T104). Not to a left operand, a condition, or
// through anything that makes one value of its operands.
const checkListContext = (call: Call): void => {
    const visit = (in_: Expr): void => {
        const e = plain(in_);
        if (e.kind === 'ternary') {
            visit(e.then);
            visit(e.else);
        } else if (e.kind === 'binary' && infixOp(e.op)?.when) {
            visit(e.right);
        } else if (e.kind === 'binary' && infixOp(e.op)?.list && plain(e.left).bracketed) {
            refuse(`(...) ${e.op} as ${call.name}'s argument repeats a list, to perl: take the brackets off the left operand`, e.pos);
        }
    };
    visit(call.args[0]!);
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

// A statement below the top of the file. `modified`: it stands before an
// `if` or `unless` modifier, where a `my` may be skipped and leave the
// last value behind (T30).
const checkStmt = (s: Stmt, modified = false): void => {
    switch (s.kind) {
    case 'use': return refuse(`'use ${s.version};' here: the version is the first statement, and is said once`, s.pos);
    case 'pragma': return refuse(`'use ${s.name}' goes at the top, after 'use ${VERSION};' and before anything else`, s.pos);
    case 'call':
        s.args.forEach(a => checkExpr(a, false));
        return checkListContext(s);
    case 'do':
        // perl warns of a statement that only has a value: `Useless use
        // of ... in void context` (T114).
        if (s.expr.kind !== 'assign' && s.expr.kind !== 'step' && s.expr.kind !== 'my') {
            refuse('this statement only has a value, and nothing is done with it: perl warns that it is useless', s.pos);
        }
        // The `my` a statement begins with is the one that may stand in it.
        const my = s.expr.kind === 'my' ? s.expr : s.expr.kind === 'assign' && s.expr.target.kind === 'my' ? s.expr.target : undefined;
        if (my !== undefined) {
            if (modified) {
                refuse('my under a modifier: when the test fails, perl leaves in the variable what it last held; declare it in a statement of its own', my.pos);
            }
            if (s.expr.kind !== 'assign') return;
            checkConcat(s.expr);
            return checkExpr(s.expr.value, false);
        }
        return checkExpr(s.expr, false);
    case 'block': return s.body.forEach(b => checkStmt(b));
    case 'if':
        for (const arm of s.arms) {
            tested(arm.test);
            checkExpr(arm.test, !s.modifier);
            arm.body.forEach(b => checkStmt(b, s.modifier === true));
        }
        return s.otherwise?.forEach(b => checkStmt(b));
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
        if (stmt.kind === 'pragma' && pragmas) {
            if (seen.has(stmt.name)) refuse(`'use ${stmt.name}' is said once`, stmt.pos);
            seen.add(stmt.name);
            checkPragma(stmt);
        } else {
            pragmas = false;
            checkStmt(stmt);
        }
    }
};
