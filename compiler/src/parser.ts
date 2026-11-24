// Tokens to the tree: statements by recursive descent, expressions by
// precedence climbing over perlop's table (D29). What a word or an
// operator means comes from the table of names; the rules of the language
// (which `use`, which integers) are the checker's.
import { refuse } from './errors.ts';
import { NAMED_UNARY_ROW, NAMES, OPERATORS, PRAGMAS, infixOp, prefixOp } from './names.ts';
import type { Token } from './lexer.ts';
import type { Expr, Program, Stmt } from './ast.ts';

// A token as a diagnostic names it. A string is shown if it is short.
const show = (t: Token): string =>
    t.kind === 'eof' ? 'the end of the file'
    : t.kind === 'int' || t.kind === 'num' || t.kind === 'version' ? t.text
    : t.kind === 'str' ? (t.text.length <= 20 && !t.text.includes('\n') ? t.text : 'a string')
    : `'${t.text}'`;

// Something else was wanted where `t` stands. A word that is one of perl's
// operators and not one of the language's (`and`, `lt`) gets the answer
// the symbols get from the lexer.
const unexpected = (t: Token, wanted: string): never =>
    t.kind === 'word' && OPERATORS.has(t.text) && !infixOp(t.text) && !prefixOp(t.text)
        ? refuse(`'${t.text}' is not in the language yet`, t.pos)
        : refuse(`expected ${wanted}, found ${show(t)}`, t.pos);

export const parse = (tokens: readonly Token[]): Program => {
    let i = 0;
    // The lexer ends every list with `eof`, and nothing reads past it.
    const peek = (): Token => tokens[i]!;
    const next = (): Token => tokens[i++]!;

    const semicolon = (): void => {
        const t = next();
        if (t.kind !== ';') unexpected(t, "';'");
    };

    const closing = (): Token => {
        const t = next();
        return t.kind === ')' ? t : unexpected(t, "')'");
    };

    // Expressions with commas between them, as many as there are.
    const list = (): Expr[] => {
        const items = [expression(Infinity)];
        while (peek().kind === ',') {
            next();
            items.push(expression(Infinity));
        }
        return items;
    };

    // A builtin that has a value, its name just read.
    const apply = (head: Token): Expr => {
        const name = NAMES.get(head.text)!;
        const open = peek();
        if (name.kind === 'unary') {
            // One of perl's named unary operators (D41). Brackets after
            // it hold its argument, whatever follows them: `length ("ab")
            // . "c"` is `2c`. Without them the argument is everything
            // that binds tighter than these operators do, which is all of
            // arithmetic and `.`: `length "ab" . "c"` is 3 (T87).
            if (open.kind === '(') {
                next();
                if (peek().kind === ')') refuse(`${head.text} needs an argument`, head.pos);
                const inner = expression(Infinity);
                closing();
                return { kind: 'apply', name: head.text, args: [inner], pos: head.pos };
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

    // A literal, a bracketed expression, a builtin and its arguments, or
    // a prefix operator and its operand, which may hold only operators
    // that bind tighter than it.
    const primary = (): Expr => {
        const t = next();
        // JavaScript reads `0x1F`, `0b101` and `0o17` as perl does, and a
        // decimal to the nearest double, as perl does too.
        const digits = t.text.replaceAll('_', '');
        if (t.kind === 'int') return { kind: 'int', text: t.text, value: BigInt(digits), pos: t.pos };
        if (t.kind === 'num') return { kind: 'num', text: t.text, value: Number(digits), pos: t.pos };
        if (t.kind === 'str') return { kind: 'str', text: t.text, value: t.value, pos: t.pos };
        if (t.kind === '(') {
            const inner = expression(Infinity);
            closing();
            return { ...inner, bracketed: true };
        }
        const prefix = t.kind === 'op' ? prefixOp(t.text) : undefined;
        if (prefix) return { kind: 'unary', op: t.text, operand: expression(prefix.row), pos: t.pos };
        if (t.kind === 'word' && NAMES.has(t.text) && NAMES.get(t.text)!.kind !== 'use') return apply(t);
        return unexpected(t, 'a value');
    };

    // Everything that binds tighter than row `limit` of the table. A row
    // that groups from the left gives its right operand only the rows
    // above it; one that groups from the right gives it its own row too.
    const expression = (limit: number): Expr => {
        let left = primary();
        for (;;) {
            const t = peek();
            const infix = t.kind === 'op' ? infixOp(t.text) : undefined;
            if (!infix || infix.row >= limit) return left;
            next();
            const right = expression(infix.assoc === 'right' ? infix.row + 1 : infix.row);
            left = { kind: 'binary', op: t.text, left, right, pos: t.pos };
        }
    };

    // The one argument of `say` or `print`, in brackets or not (D21).
    const argument = (head: Token): Expr => {
        const open = peek();
        if (open.kind !== '(') return expression(Infinity);
        next();
        const inner = expression(Infinity);
        const close = closing();
        const after = peek();
        // To perl the brackets hold all of the arguments, and an operator
        // after them is applied to what the builtin returned: `say (1 + 2)
        // * 3;` prints 3 (T25).
        if (after.kind === 'op') {
            refuse(`'${after.text}' after ${head.text} (...): perl takes the brackets for all of ${head.text}'s arguments; bracket the whole expression`, after.pos);
        }
        // After exactly one blank, perl looks along the line for the
        // closing bracket and what follows it, and warns `say (...)
        // interpreted as function` unless that is there, and a semicolon
        // (T76). With no blank, or two, or a newline, it doesn't look.
        const oneBlank = open.pos.line === head.pos.line && open.pos.col === head.pos.col + head.text.length + 1;
        if (oneBlank && after.kind === ';' && (close.pos.line !== open.pos.line || after.pos.line !== open.pos.line)) {
            refuse(`${head.text} (...) after one blank must end on the same line, ';' and all, or perl warns: write ${head.text}(...)`, open.pos);
        }
        return { ...inner, bracketed: true };
    };

    const statement = (): Stmt => {
        const head = next();
        if (head.kind !== 'word') return unexpected(head, 'a statement');
        const name = NAMES.get(head.text);
        if (name === undefined) return refuse(`'${head.text}' is not in the language`, head.pos);
        if (name.kind === 'use') {
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
        if (name.kind !== 'statement') return refuse(`${head.text} has a value, and nothing is done with it here`, head.pos);
        const args = [argument(head)];
        if (peek().kind === ',') refuse(`',' after ${head.text}'s argument: a list is not in the language yet`, peek().pos);
        semicolon();
        return { kind: 'call', name: head.text, args, pos: head.pos };
    };

    const body: Stmt[] = [];
    while (peek().kind !== 'eof') body.push(statement());
    return { kind: 'program', body, end: peek().pos };
};
