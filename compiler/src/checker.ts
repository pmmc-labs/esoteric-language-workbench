// The refusals that are rules of the language and not of its grammar
// (D29): a tree perl would accept and the language doesn't. It returns
// nothing; a tree that comes through is a program.
import { refuse } from './errors.ts';
import { BASED_MAX, DECIMAL_MAX_LENGTH, INT_MAX, PRAGMAS, VERSION, infixOp, prefixOp } from './names.ts';
import type { Expr, Invoke, My, Pragma, Program, Stmt, Sub, Var } from './ast.ts';
import type { Resolution } from './resolver.ts';

// What the checks need of the whole program (D20): the names, and for
// each sub the file variables a call of it can change, its own
// assignments and steps and those of every sub it calls (D69).
type World = { names: Resolution; changed: readonly ReadonlySet<number>[] };

// The expressions an expression is made of, in the order they are worked
// out.
const parts = (e: Expr): readonly Expr[] =>
    e.kind === 'unary' ? [e.operand]
    : e.kind === 'binary' ? [e.left, e.right]
    : e.kind === 'ternary' ? [e.test, e.then, e.else]
    : e.kind === 'apply' || e.kind === 'invoke' ? e.args
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

// Whether perl may fold an expression to a constant as it compiles: one
// with no variable in it, and one whose variables are all behind a test
// that folds, `0 && $y`, `1 ? 2 : $y` (T112). perl folds `1 && $y` to
// `$y`, which is no constant: this says yes to a little more than perl
// does, with no folder of its own.
const folds = (e: Expr): boolean =>
    e.kind === 'var' || e.kind === 'my' || e.kind === 'assign' || e.kind === 'step' || e.kind === 'invoke' ? false
    : e.kind === 'ternary' ? folds(e.test)
    : e.kind === 'binary' && infixOp(e.op)?.when ? folds(e.left)
    : parts(e).every(folds);

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

// The calls of the program's subs in an expression, and its variables.
const invokes = (e: Expr, into: Invoke[] = []): Invoke[] => {
    if (e.kind === 'invoke') into.push(e);
    parts(e).forEach(p => invokes(p, into));
    return into;
};
const variables = (e: Expr, into: (Var | My)[] = []): (Var | My)[] => {
    if (e.kind === 'var' || e.kind === 'my') into.push(e);
    parts(e).forEach(p => variables(p, into));
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
// What an expression may be worth, behind brackets, a unary plus, and
// whatever gives one operand or the other (which perl may have folded
// away).
const wholes = (e: Expr): Expr[] => {
    const p = plain(e);
    if (p.kind === 'binary' && infixOp(p.op)?.when) return [...wholes(p.left), ...wholes(p.right)];
    if (p.kind === 'ternary') return [...wholes(p.then), ...wholes(p.else)];
    return [p];
};

// `$t .= ($u = $x . $z);` never assigns `$u`, in perl 5.42 and 5.38: it
// makes one operation of the `.=` and the dot, and the `=` between them
// is lost (T129). So the right side of `.=` may not be an assignment of
// a concatenation.
const checkLostAssignment = (e: Expr): void => {
    if (e.kind !== 'assign' || !infixOp(e.op)?.concat) return;
    for (const w of wholes(e.value)) {
        // (To a `my` it is made; and a `my` may not stand there.)
        const plainAssign = w.kind === 'assign' && w.target.kind === 'var' && infixOp(w.op)?.rt === undefined && infixOp(w.op)?.when === undefined;
        if (plainAssign && wholes(w.value).some(v => v.kind === 'binary' && infixOp(v.op)?.concat)) {
            refuse(`'${e.op}' of an assignment of a concatenation: perl makes one operation of the three and never assigns $${w.target.name}; make the assignment a statement of its own`, w.pos);
        }
    }
};

const checkConcat = (w: World, e: Expr): void => {
    checkLostAssignment(e);
    const row = e.kind === 'binary' && infixOp(e.op)?.concat ? pieces(e)
        : e.kind === 'assign' && infixOp(e.op)?.concat ? [e.target, ...pieces(e.value)]
        : [];
    const read = new Set<string>();
    // The same through a call (D69, T132): the declarations the earlier
    // pieces read, and the file variables a sub called in this piece can
    // change.
    const readIds = new Set<number>();
    for (const piece of row) {
        for (const name of changes(piece)) {
            if (read.has(name)) {
                refuse(`a later piece of a concatenation changes $${name}, which an earlier piece reads: perl joins the pieces as one operation and reads each late; make the change a statement of its own`, piece.pos);
            }
        }
        for (const call of invokes(piece)) {
            for (const id of w.changed[w.names.calls.get(call)!]!) {
                if (readIds.has(id)) {
                    refuse(`a later piece of a concatenation calls ${call.name}, which can change $${w.names.names[id]}, which an earlier piece reads: perl joins the pieces as one operation and reads each late; make the call a statement of its own`, call.pos);
                }
            }
        }
        reads(piece, read);
        variables(piece).forEach(v => readIds.add(w.names.of.get(v)!));
    }
};

// A `=` whose right side is a constant, where its value is tested for
// truth: `if ($x = 5)` (D53). perl warns `Found = in conditional` when
// the right side is a constant after folding what it can, `$x = 0 && $y`
// too (T112); this is that and a little more. `tested` goes down
// through what hands a test on: a unary plus, `!` and `not` (perl takes
// the `!` of a condition away and tests the other way), the right of an
// operator that gives one operand or the other, and the branches of `? :`.
const tested = (in_: Expr): void => {
    const e = plain(in_);
    if (e.kind === 'unary' && prefixOp(e.op)?.tests) return tested(e.operand);
    if (e.kind === 'assign' && infixOp(e.op)?.rt === undefined && infixOp(e.op)?.when === undefined && folds(e.value)) {
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
const checkExpr = (w: World, e: Expr, my: boolean): void => {
    checkLiteral(e);
    checkConcat(w, e);
    if (e.kind === 'invoke') e.args.forEach(a => checkListContext(a, `as an argument of ${e.name}`));
    if (e.kind === 'my' && !my) {
        refuse(`my $${e.name} here: a my begins a statement or a for, or stands in the test of an if or a while, where it is always reached`, e.pos);
    }
    if (e.kind === 'ternary') {
        tested(e.test);
        checkExpr(w, e.test, my);
        checkExpr(w, e.then, false);
        return checkExpr(w, e.else, false);
    }
    if (e.kind === 'binary' && infixOp(e.op)?.when) {
        tested(e.left);
        checkExpr(w, e.left, my);
        return checkExpr(w, e.right, false);
    }
    if (e.kind === 'assign' && infixOp(e.op)?.when) {
        checkExpr(w, e.target, my);
        return checkExpr(w, e.value, false);
    }
    parts(e).forEach(p => checkExpr(w, p, my));
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
//
// An argument of a call, the value of a `return` and a sub's last
// statement are lists to perl too, and there a call can count: `g(("a") x
// 0)` hands `g` no argument at all (T143, D73).
const checkListContext = (arg: Expr, where: string): void => {
    const visit = (in_: Expr): void => {
        const e = plain(in_);
        if (e.kind === 'ternary') {
            visit(e.then);
            visit(e.else);
        } else if (e.kind === 'binary' && infixOp(e.op)?.when) {
            visit(e.right);
        } else if (e.kind === 'binary' && infixOp(e.op)?.list && plain(e.left).bracketed) {
            refuse(`(...) ${e.op} ${where} repeats a list, to perl: take the brackets off the left operand`, e.pos);
        }
    };
    visit(arg);
};

// A pragma as it is said: `use utf8`, `no warnings`.
const said = (pragma: string): string => (pragma.startsWith('no ') ? pragma : `use ${pragma}`);

// A pragma is written one way (D16): its arguments are the table's, each
// a string literal. perl takes `use open qw(:std :encoding(UTF-8))` and
// `use open ':std', ':utf8'` too, and each is another thing to read.
const checkPragma = (p: Pragma): void => {
    const wanted = PRAGMAS.get(p.name)!.args;
    const written = p.args.map(a => (a.kind === 'str' && !a.bracketed ? a.value : undefined));
    if (written.length !== wanted.length || written.some((w, n) => w !== wanted[n])) {
        refuse(`'${said(p.name)}' is written: ${[said(p.name), wanted.map(a => `'${a}'`).join(', ')].join(' ').trim()};`, p.pos);
    }
};

// One of the expressions of the first part of a `for`, or of its third:
// what could be a statement, and a `my` in the first part only (D60).
const checkPart = (w: World, e: Expr, first: boolean): void => {
    // A call is something done, as it is where it is a statement (D72).
    if (e.kind !== 'assign' && e.kind !== 'step' && e.kind !== 'my' && e.kind !== 'invoke') {
        refuse('this part of the for only has a value, and nothing is done with it: perl warns that it is useless', e.pos);
    }
    const my = e.kind === 'my' ? e : e.kind === 'assign' && e.target.kind === 'my' ? e.target : undefined;
    if (my === undefined) return checkExpr(w, e, false);
    if (!first) refuse(`my $${my.name} in the third part of a for: a my is in the first part, and is one variable for the whole loop`, my.pos);
    if (e.kind !== 'assign') return;
    checkConcat(w, e);
    checkExpr(w, e.value, false);
};

// A statement below the top of the file. `modified`: it stands before an
// `if` or `unless` modifier, where a `my` may be skipped and leave the
// last value behind (T30).
const checkStmt = (w: World, s: Stmt, modified = false, last = false): void => {
    switch (s.kind) {
    case 'use': return refuse(`'use ${s.version};' here: the version is the first statement, and is said once`, s.pos);
    case 'pragma': return refuse(`'${said(s.name)}' goes at the top, after 'use ${VERSION};' and before anything else`, s.pos);
    case 'call':
        s.args.forEach(a => checkExpr(w, a, false));
        return checkListContext(s.args[0]!, `as ${s.name}'s argument`);
    case 'do':
        // perl warns of a statement that only has a value: `Useless use
        // of ... in void context` (T114).
        // A call is a statement. And a value alone is one where it is
        // the last of a sub, with no modifier: it is the sub's value
        // (D72, T140), a list to perl (T143).
        if (s.expr.kind !== 'assign' && s.expr.kind !== 'step' && s.expr.kind !== 'my' && s.expr.kind !== 'invoke' && !last) {
            refuse('this statement only has a value, and nothing is done with it: perl warns that it is useless', s.pos);
        }
        if (last) checkListContext(s.expr, "as a sub's last statement");
        // The `my` a statement begins with is the one that may stand in it.
        const my = s.expr.kind === 'my' ? s.expr : s.expr.kind === 'assign' && s.expr.target.kind === 'my' ? s.expr.target : undefined;
        if (my !== undefined) {
            if (modified) {
                refuse('my under a modifier: when the test fails, perl leaves in the variable what it last held; declare it in a statement of its own', my.pos);
            }
            if (s.expr.kind !== 'assign') return;
            checkConcat(w, s.expr);
            return checkExpr(w, s.expr.value, false);
        }
        return checkExpr(w, s.expr, false);
    case 'block': return s.body.forEach(b => checkStmt(w, b));
    case 'if':
        for (const arm of s.arms) {
            tested(arm.test);
            checkExpr(w, arm.test, !s.modifier);
            arm.body.forEach(b => checkStmt(w, b, s.modifier === true));
        }
        return s.otherwise?.forEach(b => checkStmt(w, b));
    // A loop's test is a test as an `if`'s is (D53, D62), and a `my` under
    // a `while` modifier is as one under `if` (T119).
    case 'while':
        tested(s.test);
        checkExpr(w, s.test, !s.modifier);
        return s.body.forEach(b => checkStmt(w, b, s.modifier === true));
    case 'for':
        s.first.forEach(e => checkPart(w, e, true));
        if (s.test) {
            tested(s.test);
            checkExpr(w, s.test, false);
        }
        s.each.forEach(e => checkPart(w, e, false));
        return s.body.forEach(b => checkStmt(w, b));
    // Which loop it is for is the resolver's to say.
    case 'jump': return;
    case 'return':
        if (s.value === undefined) return;
        checkExpr(w, s.value, false);
        return checkListContext(s.value, 'after return');
    // The parser lets a sub stand at the top level only.
    case 'sub': throw new Error('a sub below the top level');
    }
};

// A sub (D72): its parameters, and its body, whose last statement may be
// a value alone. (Its name is the parser's to refuse.)
const checkSub = (w: World, s: Sub): void => {
    let optional = false;
    for (const p of s.params) {
        if (p.op === undefined && optional) refuse('a required parameter after an optional one: perl refuses it', p.pos);
        optional = optional || p.op !== undefined;
        if (p.default) checkExpr(w, p.default, false);
    }
    s.body.forEach((b, n) => checkStmt(w, b, false, n === s.body.length - 1));
};

// The file variables each sub can change: its own assignments and steps,
// in its body and its defaults, and those of the subs it calls, and so on
// until nothing is added.
const changedBy = (names: Resolution): ReadonlySet<number>[] => {
    const own: Set<number>[] = [new Set()];
    const callees: Set<number>[] = [new Set()];
    const expr = (e: Expr, fn: number): void => {
        if (e.kind === 'assign' || e.kind === 'step') {
            const id = names.of.get(e.target)!;
            if (names.owner[id] === 0) own[fn]!.add(id);
        }
        if (e.kind === 'invoke') callees[fn]!.add(names.calls.get(e)!);
        parts(e).forEach(p => expr(p, fn));
    };
    const stmt = (s: Stmt, fn: number): void => {
        switch (s.kind) {
        case 'call': return s.args.forEach(a => expr(a, fn));
        case 'do': return expr(s.expr, fn);
        case 'return': return s.value === undefined ? undefined : expr(s.value, fn);
        case 'block': return s.body.forEach(b => stmt(b, fn));
        case 'if':
            for (const arm of s.arms) {
                expr(arm.test, fn);
                arm.body.forEach(b => stmt(b, fn));
            }
            return s.otherwise?.forEach(b => stmt(b, fn));
        case 'while':
            expr(s.test, fn);
            return s.body.forEach(b => stmt(b, fn));
        case 'for':
            [...s.first, ...(s.test ? [s.test] : []), ...s.each].forEach(e => expr(e, fn));
            return s.body.forEach(b => stmt(b, fn));
        default: return;
        }
    };
    for (const [n, s] of names.subs.entries()) {
        own.push(new Set());
        callees.push(new Set());
        s.params.forEach(p => p.default && expr(p.default, n + 1));
        s.body.forEach(b => stmt(b, n + 1));
    }
    for (let grew = true; grew;) {
        grew = false;
        for (const [fn, set] of own.entries()) {
            for (const callee of callees[fn]!) {
                for (const id of own[callee]!) {
                    if (!set.has(id)) {
                        set.add(id);
                        grew = true;
                    }
                }
            }
        }
    }
    return own;
};

export const check = (program: Program, names: Resolution): void => {
    const w: World = { names, changed: changedBy(names) };
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
            if (seen.has(stmt.name)) refuse(`'${said(stmt.name)}' is said once`, stmt.pos);
            seen.add(stmt.name);
            checkPragma(stmt);
        } else if (stmt.kind === 'sub') {
            pragmas = false;
            checkSub(w, stmt);
        } else {
            pragmas = false;
            checkStmt(w, stmt);
        }
    }
};
