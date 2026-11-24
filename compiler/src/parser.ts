// Tokens to the tree: statements by recursive descent (D29). What a word
// at the start of a statement means comes from the table of names; the
// rules of the language (which `use`, which integers) are the checker's.
// Step 1 brings expressions, by precedence climbing.
import { refuse } from './errors.ts';
import { NAMES } from './names.ts';
import type { Token } from './lexer.ts';
import type { Expr, Program, Stmt } from './ast.ts';

// A token as a diagnostic names it.
const show = (t: Token): string =>
    t.kind === 'eof' ? 'the end of the file'
    : t.kind === 'word' || t.kind === ';' ? `'${t.text}'`
    : t.text;

export const parse = (tokens: readonly Token[]): Program => {
    let i = 0;
    // The lexer ends every list with `eof`, and nothing reads past it.
    const peek = (): Token => tokens[i]!;
    const next = (): Token => tokens[i++]!;

    const semicolon = (): void => {
        const t = next();
        if (t.kind !== ';') refuse(`expected ';', found ${show(t)}`, t.pos);
    };

    const statement = (): Stmt => {
        const head = next();
        if (head.kind !== 'word') return refuse(`expected a statement, found ${show(head)}`, head.pos);
        const name = NAMES.get(head.text);
        if (name === undefined) return refuse(`'${head.text}' is not in the language`, head.pos);
        if (name.kind === 'use') {
            const version = next();
            if (version.kind !== 'version') return refuse(`after 'use', expected a version, found ${show(version)}`, version.pos);
            semicolon();
            return { kind: 'use', version: version.text, pos: head.pos };
        }
        const arg = next();
        if (arg.kind !== 'int') return refuse(`after '${head.text}', expected an integer, found ${show(arg)}`, arg.pos);
        const args: Expr[] = [{ kind: 'int', text: arg.text, value: BigInt(arg.text), pos: arg.pos }];
        semicolon();
        return { kind: 'call', name: head.text, args, pos: head.pos };
    };

    const body: Stmt[] = [];
    while (peek().kind !== 'eof') body.push(statement());
    return { kind: 'program', body, end: peek().pos };
};
