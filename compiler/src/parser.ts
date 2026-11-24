// Tokens to the tree: statements by recursive descent, expressions by
// precedence climbing over perlop's table (D29). What a word or an
// operator means comes from the table of names; the rules of the language
// (which `use`, which integers) are the checker's.
import { refuse } from './errors.ts';
import { NAMES, OPERATORS, infixOp, prefixOp } from './names.ts';
import type { Token } from './lexer.ts';
import type { Expr, Program, Stmt } from './ast.ts';

// A token as a diagnostic names it.
const show = (t: Token): string =>
    t.kind === 'eof' ? 'the end of the file'
    : t.kind === 'int' || t.kind === 'num' || t.kind === 'version' ? t.text
    : `'${t.text}'`;

// Something else was wanted where `t` stands. A word that is one of perl's
// operators (`x`, `and`) gets the answer the symbols get from the lexer.
const unexpected = (t: Token, wanted: string): never =>
    t.kind === 'word' && OPERATORS.has(t.text)
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

    // A number, a bracketed expression, or a prefix operator and its
    // operand, which may hold only operators that bind tighter than it.
    const primary = (): Expr => {
        const t = next();
        // JavaScript reads `0x1F`, `0b101` and `0o17` as perl does, and a
        // decimal to the nearest double, as perl does too.
        const digits = t.text.replaceAll('_', '');
        if (t.kind === 'int') return { kind: 'int', text: t.text, value: BigInt(digits), pos: t.pos };
        if (t.kind === 'num') return { kind: 'num', text: t.text, value: Number(digits), pos: t.pos };
        if (t.kind === '(') {
            const inner = expression(Infinity);
            closing();
            return { ...inner, bracketed: true };
        }
        const prefix = t.kind === 'op' ? prefixOp(t.text) : undefined;
        if (prefix) return { kind: 'unary', op: t.text, operand: expression(prefix.row), pos: t.pos };
        return unexpected(t, "a number or '('");
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

    // A builtin's one argument, in brackets or not (D21).
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
            const version = next();
            if (version.kind !== 'version') return refuse(`after 'use', expected a version, found ${show(version)}`, version.pos);
            semicolon();
            return { kind: 'use', version: version.text, pos: head.pos };
        }
        const args = [argument(head)];
        semicolon();
        return { kind: 'call', name: head.text, args, pos: head.pos };
    };

    const body: Stmt[] = [];
    while (peek().kind !== 'eof') body.push(statement());
    return { kind: 'program', body, end: peek().pos };
};
