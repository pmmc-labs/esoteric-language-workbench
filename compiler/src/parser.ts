// Tokens to the tree: statements by recursive descent, expressions by
// precedence climbing over perlop's table (D29). What a word or an
// operator means comes from the table of names; the rules of the language
// (which `use`, which integers) are the checker's.
import { refuse } from './errors.ts';
import { AND_ROW, COMMA_ROW, NAMED_UNARY_ROW, NAMES, OPERATORS, PRAGMAS, PRECEDENCE, TERNARY_ROW, infixOp, prefixOp, stepOp } from './names.ts';
import type { Token } from './lexer.ts';
import type { Arm, Expr, Program, Stmt, Var } from './ast.ts';

// A token as a diagnostic names it. A string is shown if it is short.
const show = (t: Token): string =>
    t.kind === 'eof' ? 'the end of the file'
    : t.kind === 'int' || t.kind === 'num' || t.kind === 'version' ? t.text
    : t.kind === 'str' ? (t.text.length <= 20 && !t.text.includes('\n') ? t.text : 'a string')
    : `'${t.text}'`;

// Something else was wanted where `t` stands. A word that is one of perl's
// operators and not one of the language's (`isa`) gets the answer the
// symbols get from the lexer.
const unexpected = (t: Token, wanted: string): never =>
    t.kind === 'word' && OPERATORS.has(t.text) && !infixOp(t.text) && !prefixOp(t.text)
        ? refuse(`'${t.text}' is not in the language yet`, t.pos)
        : refuse(`expected ${wanted}, found ${show(t)}`, t.pos);

export const parse = (tokens: readonly Token[]): Program => {
    let i = 0;
    // The lexer ends every list with `eof`, and nothing reads past it.
    const peek = (): Token => tokens[i]!;
    const next = (): Token => tokens[i++]!;
    // Whether the expression being read is an argument in a list of them,
    // with no bracket of its own round it yet: there a word operator would
    // take the rest of the list, commas and all (D51).
    let inList = false;

    const semicolon = (): void => {
        const t = next();
        if (t.kind !== ';') unexpected(t, "';'");
    };

    const closing = (): Token => {
        const t = next();
        return t.kind === ')' ? t : unexpected(t, "')'");
    };

    // An expression in brackets, the opening one read: inside, it is no
    // one's list.
    const bracketed = (): Expr => {
        const outer = inList;
        inList = false;
        const inner = expression(Infinity);
        inList = outer;
        closing();
        return inner;
    };

    // Expressions with commas between them, as many as there are. Each
    // may hold what binds tighter than a comma, and the word operators
    // don't: perl reads `f(1, 0 or 2)` as `f((1, 0) or 2)`.
    const list = (): Expr[] => {
        const outer = inList;
        inList = true;
        const items = [expression(COMMA_ROW)];
        while (peek().kind === ',') {
            next();
            items.push(expression(COMMA_ROW));
        }
        inList = outer;
        const t = peek();
        if (t.kind === 'op' && (infixOp(t.text)?.row ?? 0) > COMMA_ROW) {
            refuse(`'${t.text}' in a list of arguments takes the whole list for its left side, to perl: bracket what it joins`, t.pos);
        }
        return items;
    };

    // A builtin that has a value, its name just read.
    const apply = (head: Token): Expr => {
        const name = NAMES.get(head.text)!;
        const open = peek();
        if (name.kind === 'constant') {
            // `true ()` is a call to perl, and `undef (...)` the operator
            // that makes a variable undefined.
            if (open.kind === '(') refuse(`${head.text} is written without brackets`, open.pos);
            // perl takes what follows `undef` for its argument whenever it
            // can: `undef * 2` is undef of a glob called 2, and `undef +
            // 1` doesn't compile (T105). What can't be one is the end of
            // an expression, the operators that take an undef, and a
            // modifier: `$x = undef if $y;`.
            const follows = open.kind === 'op' ? infixOp(open.text)?.logic
                : open.kind === 'word' ? NAMES.get(open.text)?.kind === 'if'
                : open.kind !== 'int' && open.kind !== 'num' && open.kind !== 'str' && open.kind !== 'version' && open.kind !== 'var' && open.kind !== '{';
            if (name.bare && !follows) {
                refuse(`${head.text} before ${show(open)}: perl takes what follows ${head.text} for its argument; write (${head.text})`, head.pos);
            }
            return { kind: 'constant', name: head.text, pos: head.pos };
        }
        if (name.kind === 'unary') {
            // One of perl's named unary operators (D41). Brackets after
            // it hold its argument, whatever follows them: `length ("ab")
            // . "c"` is `2c`. Without them the argument is everything
            // that binds tighter than these operators do, which is all of
            // arithmetic and `.`: `length "ab" . "c"` is 3 (T87).
            if (open.kind === '(') {
                next();
                if (peek().kind === ')') refuse(`${head.text} needs an argument`, head.pos);
                return { kind: 'apply', name: head.text, args: [bracketed()], pos: head.pos };
            }
            if (open.kind === ';' || open.kind === ')' || open.kind === ',' || open.kind === 'eof') {
                refuse(`${head.text} needs an argument`, head.pos);
            }
            return { kind: 'apply', name: head.text, args: [expression(NAMED_UNARY_ROW)], pos: head.pos };
        }
        if (name.kind !== 'function') return refuse(`${head.text} is a statement, and has no value`, head.pos);
        // perl takes `substr $s, 0, 1` as well: a list operator's
        // arguments without brackets, which D21 is wary of.
        if (open.kind !== '(') refuse(`${head.text} needs brackets round its arguments: ${head.text}(...)`, head.pos);
        next();
        const args = peek().kind === ')' ? [] : list();
        closing();
        const max = name.min + name.rt.length - 1;
        if (args.length < name.min || args.length > max) {
            refuse(`${head.text} takes ${name.min} to ${max} arguments, and here are ${args.length}`, head.pos);
        }
        return { kind: 'apply', name: head.text, args, pos: head.pos };
    };

    // A prefix operator and its operand, the operator just read: the
    // operand may hold only what binds tighter than the operator.
    const prefixed = (t: Token, row: number): Expr => {
        // `not`, the one prefix operator below the comma. In a list of
        // arguments it takes the rest of the list for its operand, to
        // perl; and a bracket straight after it is all it takes, so that
        // `not (0) || 1` is `(not 0) || 1` (T107). The first is refused,
        // and so is the second when an operator `not` would have taken
        // follows the bracket (D51).
        if (row > COMMA_ROW) {
            if (peek().kind === '(') {
                next();
                if (peek().kind === ')') refuse(`${t.text} needs an operand`, t.pos);
                const operand: Expr = { ...bracketed(), bracketed: true };
                const after = peek();
                if (after.kind === '?' || (after.kind === 'op' && (infixOp(after.text)?.row ?? Infinity) < row)) {
                    refuse(`'${after.text}' after ${t.text} (...): perl takes the brackets for all of ${t.text}'s operand; bracket the whole of it, ${t.text} ((...) ${after.text} ...), or the ${t.text} itself`, after.pos);
                }
                return { kind: 'unary', op: t.text, operand, pos: t.pos };
            }
            if (inList) refuse(`${t.text} in a list of arguments takes the rest of the list, to perl: write ${t.text}(...)`, t.pos);
        }
        return { kind: 'unary', op: t.text, operand: expression(row), pos: t.pos };
    };

    // A literal, a bracketed expression, a builtin and its arguments, or
    // a prefix operator and its operand.
    const primary = (): Expr => {
        const t = next();
        // JavaScript reads `0x1F`, `0b101` and `0o17` as perl does, and a
        // decimal to the nearest double, as perl does too.
        const digits = t.text.replaceAll('_', '');
        if (t.kind === 'int') return { kind: 'int', text: t.text, value: BigInt(digits), pos: t.pos };
        if (t.kind === 'num') return { kind: 'num', text: t.text, value: Number(digits), pos: t.pos };
        if (t.kind === 'str') return { kind: 'str', text: t.text, value: t.value, pos: t.pos };
        if (t.kind === '(') return { ...bracketed(), bracketed: true };
        // A variable, and `++` or `--` hard after it or not: they bind
        // tighter than anything else there is.
        if (t.kind === 'var') {
            const target: Var = { kind: 'var', name: t.name, pos: t.pos };
            const after = peek();
            if (after.kind !== 'op' || !stepOp(after.text)) return target;
            next();
            return { kind: 'step', op: after.text, before: false, target, pos: after.pos };
        }
        if (t.kind === 'op' && stepOp(t.text)) {
            const v = next();
            if (v.kind !== 'var') return refuse(`'${t.text}' is for a variable: ${t.text}$x`, t.pos);
            return { kind: 'step', op: t.text, before: true, target: { kind: 'var', name: v.name, pos: v.pos }, pos: t.pos };
        }
        const prefix = t.kind === 'op' ? prefixOp(t.text) : undefined;
        if (prefix) return prefixed(t, prefix.row);
        if (t.kind === 'word' && NAMES.get(t.text)?.kind === 'my') {
            const v = next();
            if (v.kind !== 'var') return refuse(`after 'my', expected a variable, found ${show(v)}`, v.pos);
            return { kind: 'my', name: v.name, pos: t.pos };
        }
        const name = t.kind === 'word' ? NAMES.get(t.text) : undefined;
        if (name?.kind === 'constant' || name?.kind === 'unary' || name?.kind === 'function' || name?.kind === 'statement') return apply(t);
        return unexpected(t, 'a value');
    };

    // Everything that binds tighter than row `limit` of the table. A row
    // that groups from the left gives its right operand only the rows
    // above it; one that groups from the right gives it its own row too.
    const expression = (limit: number): Expr => {
        let left = primary();
        for (;;) {
            const t = peek();
            // `? :` groups from the right, and what stands between the
            // two marks is bracketed by them.
            if (t.kind === '?' && TERNARY_ROW < limit) {
                next();
                const then = expression(TERNARY_ROW + 1);
                const colon = next();
                if (colon.kind !== ':') unexpected(colon, "':'");
                left = { kind: 'ternary', test: left, then, else: expression(TERNARY_ROW + 1), pos: t.pos };
                continue;
            }
            const infix = t.kind === 'op' ? infixOp(t.text) : undefined;
            if (!infix || infix.row >= limit) return left;
            next();
            // An assignment: its left side is a variable, and nothing
            // else. perl takes `($x = 5) = 7` and `(1 ? $x : $y) = 8`;
            // values flow here, and places don't (D17, D56). `($x) = 5`
            // is a list assignment to perl.
            if (infix.assign) {
                if ((left.kind !== 'var' && left.kind !== 'my') || left.bracketed) {
                    return refuse(`the left side of '${t.text}' is a variable, $x or my $x, with no brackets round it`, t.pos);
                }
                left = { kind: 'assign', op: t.text, target: left, value: expression(infix.row + 1), pos: t.pos };
                continue;
            }
            // `!$x == $y` is `(!$x) == $y`, and perl 5.42 warns of a
            // precedence problem as it compiles, unless it can fold the
            // `!` away (T115). A unary plus before the `!` doesn't hide it.
            let first = left;
            while (first.kind === 'unary' && !first.bracketed && prefixOp(first.op)?.rt === undefined) first = first.operand;
            if (PRECEDENCE[infix.row]!.assoc.startsWith('chain') && first.kind === 'unary' && !first.bracketed && prefixOp(first.op)?.bang) {
                refuse(`'${first.op}' before '${t.text}': perl warns of a precedence problem; write ${first.op}(... ${t.text} ...), or (${first.op}...) ${t.text} ...`, first.pos);
            }
            const right = expression(infix.assoc === 'right' ? infix.row + 1 : infix.row);
            left = { kind: 'binary', op: t.text, left, right, pos: t.pos };
            // perl chains two comparisons of one row, `1 < 5 < 3` being
            // `1 < 5 && 5 < 3`, or doesn't compile them (T33, T51, T108).
            // Read from the left they would mean something else (D50).
            const again = peek();
            if (PRECEDENCE[infix.row]!.assoc.startsWith('chain') && again.kind === 'op' && infixOp(again.text)?.row === infix.row) {
                refuse(`'${again.text}' after '${t.text}': perl chains two comparisons, or refuses them, and never reads them from the left; bracket one, or join two with &&`, again.pos);
            }
        }
    };

    // The one argument of `say` or `print`, in brackets or not (D21).
    const argument = (head: Token): Expr => {
        const open = peek();
        // The word operators bind more loosely than `say` does: `say 0 or
        // 2;` is `(say 0) or 2` (T106). So without brackets the argument
        // stops before one, and the statement refuses it.
        if (open.kind !== '(') return expression(AND_ROW);
        next();
        const inner = bracketed();
        const after = peek();
        // To perl the brackets hold all of the arguments, and an operator
        // after them is applied to what the builtin returned: `say (1 + 2)
        // * 3;` prints 3 (T25).
        if (after.kind === 'op' || after.kind === '?') {
            refuse(`'${after.text}' after ${head.text} (...): perl takes the brackets for all of ${head.text}'s arguments; bracket the whole expression`, after.pos);
        }
        // After exactly one blank, perl looks along the line, as text,
        // for the closing bracket and what follows it, and warns `say
        // (...) interpreted as function` unless they are there (T76,
        // T100). The lexer has looked as perl does. (Anything but a
        // semicolon here is refused for what it is, below.)
        if (head.kind === 'word' && head.asFunction && after.kind === ';') {
            refuse(`${head.text} (...) after one blank: perl warns unless the brackets close on this line, one in a string counting too, with ';' after them: write ${head.text}(...)`, open.pos);
        }
        return { ...inner, bracketed: true };
    };

    // A word operator after a statement's expression: `$x = 1 and $y =
    // 2;` is two assignments joined, to perl, and a statement here is
    // one (D56).
    const loose = (): void => {
        const after = peek();
        if (after.kind === 'op' && infixOp(after.text)) {
            refuse(`'${after.text}' after a statement joins it to what follows, to perl, which binds '${after.text}' more loosely than '=': write it as an if`, after.pos);
        }
    };

    // `{ statements }`, the opening brace next.
    const block = (): Stmt[] => {
        const open = next();
        if (open.kind !== '{') unexpected(open, "'{'");
        const body: Stmt[] = [];
        while (peek().kind !== '}' && peek().kind !== 'eof') body.push(statement());
        const close = next();
        if (close.kind !== '}') unexpected(close, "'}'");
        return body;
    };

    // `(test)` and a block, for `if`, `elsif` and `unless`.
    const arm = (head: Token, negate: boolean): Arm => {
        const open = next();
        if (open.kind !== '(') unexpected(open, `'(' after ${head.text}`);
        const test = bracketed();
        return negate ? { test, negate, body: block(), pos: head.pos } : { test, body: block(), pos: head.pos };
    };

    // `say`, `print`, or an expression that is a statement, as far as its
    // semicolon or a modifier.
    const simple = (): Stmt => {
        const head = peek();
        const name = head.kind === 'word' ? NAMES.get(head.text) : undefined;
        if (head.kind === 'word' && name === undefined) return refuse(`'${head.text}' is not in the language`, head.pos);
        if (name?.kind === 'statement') {
            next();
            const args = [argument(head)];
            const after = peek();
            if (after.kind === ',') refuse(`',' after ${head.text}'s argument: a list is not in the language yet`, after.pos);
            if (after.kind === 'op' && infixOp(after.text)) {
                refuse(`'${after.text}' after ${head.text}'s argument: it binds more loosely than ${head.text} does, and joins what ${head.text} returns, to perl; bracket the argument, ${head.text}(... ${after.text} ...)`, after.pos);
            }
            return { kind: 'call', name: head.text, args, pos: head.pos };
        }
        if (name?.kind === 'elsif' || name?.kind === 'else') return refuse(`${head.text} without an if before it`, head.pos);
        if (head.kind === ';' || head.kind === '}' || head.kind === ')' || head.kind === 'eof') return unexpected(next(), 'a statement');
        const expr = expression(AND_ROW);
        loose();
        return { kind: 'do', expr, pos: head.pos };
    };

    const statement = (): Stmt => {
        const head = peek();
        const name = head.kind === 'word' ? NAMES.get(head.text) : undefined;
        if (name?.kind === 'use') {
            next();
            const what = next();
            if (what.kind === 'version') {
                semicolon();
                return { kind: 'use', version: what.text, pos: head.pos };
            }
            if (what.kind !== 'word') return refuse(`after 'use', expected a version or a pragma, found ${show(what)}`, what.pos);
            if (!PRAGMAS.has(what.text)) return refuse(`'use ${what.text}' is not in the language`, what.pos);
            const args = peek().kind === ';' ? [] : list();
            semicolon();
            return { kind: 'pragma', name: what.text, args, pos: head.pos };
        }
        // A block. An empty one is an anonymous hash to perl, `{}`, and a
        // statement that is only a value (T116).
        if (head.kind === '{') {
            const body = block();
            if (body.length === 0) refuse("an empty block is an anonymous hash, to perl: put a statement in it, or take it out", head.pos);
            return { kind: 'block', body, pos: head.pos };
        }
        if (name?.kind === 'if') {
            next();
            const arms = [arm(head, name.unless === true)];
            let otherwise: Stmt[] | undefined;
            for (;;) {
                const more = peek();
                const word = more.kind === 'word' ? NAMES.get(more.text) : undefined;
                if (word?.kind !== 'elsif' && word?.kind !== 'else') break;
                // `unless` with an `else` is an `if` written backwards (D54).
                if (name.unless) refuse(`${more.text} after unless: write it as an if`, more.pos);
                next();
                if (word.kind === 'elsif') {
                    arms.push(arm(more, false));
                } else {
                    otherwise = block();
                    break;
                }
            }
            return otherwise === undefined ? { kind: 'if', arms, pos: head.pos } : { kind: 'if', arms, otherwise, pos: head.pos };
        }
        const inner = simple();
        // `STATEMENT if TEST;`, `STATEMENT unless TEST;`
        const word = peek();
        const modifier = word.kind === 'word' ? NAMES.get(word.text) : undefined;
        if (modifier?.kind !== 'if') {
            semicolon();
            return inner;
        }
        next();
        const test = expression(Infinity);
        semicolon();
        const one: Arm = modifier.unless ? { test, negate: true, body: [inner], pos: word.pos } : { test, body: [inner], pos: word.pos };
        return { kind: 'if', arms: [one], modifier: true, pos: inner.pos };
    };

    const body: Stmt[] = [];
    while (peek().kind !== 'eof') body.push(statement());
    return { kind: 'program', body, end: peek().pos };
};
