// Tokens to the tree: statements by recursive descent, expressions by
// precedence climbing over perlop's table (D29). What a word or an
// operator means comes from the table of names; the rules of the language
// (which `use`, which integers) are the checker's.
import { refuse } from './errors.ts';
import { AND_ROW, COMMA_ROW, NAMED_UNARY_ROW, NAMES, NAME_MAX_LENGTH, OPERATORS, PERL_KEYWORDS, PERL_WORDS, PRAGMAS, PRECEDENCE, TERNARY_ROW, infixOp, isLabel, isVersionString, prefixOp, stepOp } from './names.ts';
import type { Index, Token } from './lexer.ts';
import type { Arm, Elem, Expr, HashOp, Label, Param, Pos, Program, Stmt, Var } from './ast.ts';

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

// `if`, `unless`, `while` and `until`, which may follow a statement.
const isModifier = (t: Token): boolean => {
    const kind = t.kind === 'word' ? NAMES.get(t.text)?.kind : undefined;
    return kind === 'if' || kind === 'while' || kind === 'for';
};

export const parse = (tokens: readonly Token[]): Program => {
    let i = 0;
    // How many blocks of a `map` or a `grep` are open.
    let blocks = 0;
    // The lexer ends every list with `eof`, and nothing reads past it.
    const peek = (): Token => tokens[i]!;
    const next = (): Token => tokens[i++]!;
    // Whether the expression being read is an argument in a list of them,
    // with no bracket of its own round it yet: there a word operator would
    // take the rest of the list, commas and all (D51).
    let inList = false;
    // How many blocks are open, and whether a sub's is: a sub stands at
    // the top level, and a `return` in a sub (D72).
    let depth = 0;
    let inSub = false;
    // Step 15 (D150): the `die`s and `warn`s read in each unit that names
    // a line of its own to perl (a statement, a test, a loop's header, a
    // default), the innermost last. perl's line for a unit over several
    // lines is its lexer's (T317), and for a `while`'s test the last
    // statement its block ran (T316): so a message that would carry the
    // line may not be made in either.
    const units: Expr[][] = [];
    // A message that ends in a newline written as such carries no line.
    const endsInNewline = (d: Expr): boolean => {
        if (d.kind !== 'listop') return false;
        const last = d.args.at(-1);
        const text = last?.kind === 'str' ? last.value : last?.kind === 'interp' && last.parts.at(-1)?.kind === 'str' ? (last.parts.at(-1) as { value: string }).value : '';
        return text.endsWith('\n');
    };
    // Where token `t` ends: a string may hold the ends of lines.
    const lastLine = (t: Token): number => t.pos.line + (t.text.match(/\n/g)?.length ?? 0);
    const unit = <T>(from: Pos, read: () => T, loopTest = false): T => {
        units.push([]);
        const made = read();
        const found = units.pop()!;
        const to = lastLine(tokens[i - 1]!);
        for (const d of found) {
            if (endsInNewline(d)) continue;
            const word = d.kind === 'listop' ? d.op : 'die';
            if (loopTest) refuse(`a ${word} in the test of a while or an until: perl names the line of the last statement the loop's block ran, and the message would carry it; end the message in a newline, or work the test out in the block`, d.pos);
            if (to !== from.line) refuse(`a ${word} in a statement, a test or a header over more than one line: perl names a line of its own choosing there, and the message would carry it; put it on one line, or end the message in a newline`, d.pos);
        }
        return made;
    };

    // Whether token `k + 1` is hard against token `k`, a word.
    const touching = (k: number): boolean => {
        const [a, b] = [tokens[k]!, tokens[k + 1]!];
        return b.pos.line === a.pos.line && b.pos.col === a.pos.col + a.text.length;
    };

    // `-e(2)` is a file test to perl, of a file called 2, and `5-f(2)`
    // doesn't compile: a minus hard against one letter and no more, wherever
    // it stands (T135).
    for (let k = 0; k + 1 < tokens.length; k++) {
        const [minus, word] = [tokens[k]!, tokens[k + 1]!];
        if (minus.kind === 'op' && minus.text === '-' && word.kind === 'word' && /^[A-Za-z]$/.test(word.text) && touching(k)) {
            refuse(`-${word.text}: a minus hard against one letter is a file test, to perl; put a blank after the minus, or brackets round what it negates`, minus.pos);
        }
    }

    // A word that could be the name of one of the program's subs: not one
    // of the language's, and not one of perl's.
    const callable = (t: Token): boolean => t.kind === 'word' && !NAMES.has(t.text) && !PERL_WORDS.has(t.text);

    // Whether a comma stands between token `from` and the `close` that
    // ends what it begins, outside any brackets of its own: a list.
    const commaAhead = (from: number, close: ')' | ';'): boolean => {
        let nested = 0;
        for (let k = from; tokens[k]!.kind !== 'eof'; k++) {
            const kind = tokens[k]!.kind;
            if (nested === 0 && (kind === close || kind === ';' || kind === '}')) return false;
            if (nested === 0 && kind === ',') return true;
            nested += kind === '(' || kind === '[' || kind === '{' ? 1 : kind === ')' || kind === ']' || kind === '}' ? -1 : 0;
            if (nested < 0) return false;
        }
        return false;
    };

    const semicolon = (): void => {
        const t = next();
        if (t.kind !== ';') unexpected(t, "';'");
    };

    // The end of a statement: its semicolon, which the last statement of
    // a block may leave out, as in perl (D75). The brace is the block's
    // to read.
    const ending = (): void => {
        if (peek().kind === '}' && depth > 0) return;
        semicolon();
    };
    const ends = (t: Token): boolean => t.kind === ';' || (t.kind === '}' && depth > 0);

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
                : open.kind === 'word' ? isModifier(open)
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
            if (open.kind === ';' || open.kind === ')' || open.kind === ',' || open.kind === '}' || open.kind === 'eof') {
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

    // The items of a list as far as `end`, the opening bracket read: each
    // may hold what binds tighter than a comma, and one comma may follow
    // the last.
    const itemsTo = (end: ')' | ']' | '}'): Expr[] => {
        const outer = inList;
        inList = true;
        const items: Expr[] = [];
        while (peek().kind !== end) {
            if (peek().kind === ',') refuse("a comma with no value before it: perl leaves it out, in silence, where it doesn't refuse it", peek().pos);
            items.push(expression(COMMA_ROW));
            const t = peek();
            if (t.kind === 'op' && (infixOp(t.text)?.row ?? 0) > COMMA_ROW) {
                refuse(`'${t.text}' in a list takes the whole list for its left side, to perl: bracket what it joins`, t.pos);
            }
            if (t.kind !== ',') break;
            next();
        }
        inList = outer;
        const close = next();
        if (close.kind !== end) unexpected(close, `'${end}'`);
        return items;
    };

    // An element, `$name[index]`, the variable's token just read and the
    // square bracket next. perl takes a blank between the two, and reads
    // `$x [1]` as an element even where there is a `$x`.
    const element = (v: Token): Elem => {
        if (!touching(i - 1)) refuse(`a blank between $${v.text.slice(1)} and '[': an element is written $${v.text.slice(1)}[...]`, peek().pos);
        next();
        const outer = inList;
        inList = false;
        const index = expression(Infinity);
        inList = outer;
        const close = next();
        if (close.kind !== ']') unexpected(close, "']'");
        // An array holds no array (step 13).
        if (peek().kind === '[') refuse('an element of an element: an array of arrays is not in the language yet', peek().pos);
        return { kind: 'elem', name: v.text.slice(1), index, pos: v.pos };
    };

    // An element of a hash, `$name{key}`, the variable's token just read
    // and the brace next (step 12a). The key is one expression: a word
    // alone is a string already, by the lexer. perl joins `$h{1, 2}` into
    // one key.
    const hashElement = (v: Token): Elem => {
        const open = next();
        if (peek().kind === '}') refuse(`$${v.text.slice(1)}{} has no key: perl does not compile it`, open.pos);
        const outer = inList;
        inList = false;
        const index = expression(Infinity);
        inList = outer;
        const close = next();
        if (close.kind === ',') refuse("a comma in a hash's key: perl joins the values into one key", close.pos);
        if (close.kind !== '}') unexpected(close, "'}'");
        // A hash holds no hash and no array (step 13).
        if (peek().kind === '{' || peek().kind === '[') refuse('an element of an element: a hash of hashes or of arrays is not in the language yet', peek().pos);
        return { kind: 'elem', name: v.text.slice(1), index, hash: true, pos: v.pos };
    };

    // A slice of a hash, `@name{keys}`, the array's token just read and the
    // brace next (step 12b).
    const hashSlice = (t: { name: string; pos: Pos }): Expr & { kind: 'slice' } => {
        const open = next();
        const keys = itemsTo('}');
        // perl does not compile `@h{}`.
        if (keys.length === 0) refuse('a slice with no key: perl refuses it', open.pos);
        if (peek().kind === '{' || peek().kind === '[') refuse('an element of an element: a hash of hashes or of arrays is not in the language yet', peek().pos);
        return { kind: 'slice', name: t.name, hash: true, indexes: keys, pos: t.pos };
    };

    // The variable whose token was just read, or the element of an array
    // or a hash that it begins.
    const place = (v: Token): Var | Elem => {
        const after = peek();
        if (after.kind === '[') return element(v);
        if (after.kind === '{' && after.subscript) return hashElement(v);
        if (after.kind === '{') refuse(`a blank between ${v.text} and '{': an element of a hash is written ${v.text}{...}`, after.pos);
        return { kind: 'var', name: v.text.slice(1), pos: v.pos };
    };

    // What may follow an operator that takes one thing and was written
    // without brackets: perl reads on for the argument through anything
    // that binds tighter than a named unary operator, or does not compile
    // it (T152, T220, T225).
    const bareOperand = (head: Token, shown: string): void => {
        const after = peek();
        if (after.kind === '[' || (after.kind === 'op' && (infixOp(after.text)?.row ?? Infinity) < NAMED_UNARY_ROW)) {
            refuse(`${shown} before ${show(after)}: perl reads on for ${head.text}'s argument, or does not compile it; write ${head.text}(...)`, head.pos);
        }
    };

    // A builtin that names a hash, its word just read (step 12a).
    const hashOp = (head: Token): HashOp => {
        const name = NAMES.get(head.text)!;
        if (name.kind !== 'hashop') throw new Error('not a hash builtin');
        const op = head.text as 'keys' | 'values' | 'exists' | 'delete';
        const open = peek().kind === '(';
        if (open) next();
        const what = next();
        let made: HashOp;
        let shown: string;
        if (name.shape === 'hash') {
            // perl's `keys` and `values` take an array too, and give its
            // indexes.
            if (what.kind !== 'hash') return refuse(`${head.text} names a hash, found ${show(what)}: ${head.text} %h`, what.pos);
            made = { kind: 'hashop', op, name: what.name, pos: head.pos, at: what.pos };
            shown = `${head.text} %${what.name}`;
        } else {
            const brace = peek();
            // `delete @h{...}`: each key's value, in a list (step 12b).
            if (op === 'delete' && what.kind === 'array' && brace.kind === '{' && brace.subscript === true) {
                const slice = hashSlice(what);
                if (open) closing();
                else bareOperand(head, `delete @${slice.name}{...}`);
                return { kind: 'hashop', op, name: slice.name!, keys: slice.indexes, pos: head.pos, at: what.pos };
            }
            // perl's take an element of an array too.
            if (what.kind !== 'var' || brace.kind !== '{' || brace.subscript !== true) {
                return refuse(`${head.text} takes an element of a hash, found ${show(what)}: ${head.text} $h{...}`, what.pos);
            }
            const element = hashElement(what);
            made = { kind: 'hashop', op, name: element.name, key: element.index, pos: head.pos, at: what.pos };
            shown = `${head.text} $${element.name}{...}`;
        }
        if (open) {
            closing();
            if (peek().kind === '[') refuse(`'[' after ${head.text}(...): perl does not compile it; bracket the whole, (${head.text}(...))[...]`, peek().pos);
        } else {
            bareOperand(head, shown);
        }
        return made;
    };

    // A builtin that names an array, its word just read (D80).
    const arrayOp = (head: Token): Expr => {
        const name = NAMES.get(head.text)!;
        if (name.kind !== 'arrayop') throw new Error('not an array builtin');
        const open = peek().kind === '(';
        if (!open && (name.shape === 'splice' || name.shape === 'scalar')) refuse(`${head.text} needs brackets: ${head.text}(@a${name.shape === 'splice' ? ', ...' : ''})`, head.pos);
        if (open) next();
        // `scalar(%h)`, `scalar(keys %h)` and `scalar(values %h)`: how
        // many keys the hash has (T219).
        if (name.shape === 'scalar' && (peek().kind === 'hash' || (peek().kind === 'word' && (peek().text === 'keys' || peek().text === 'values')))) {
            const first = next();
            const of: { name: string; at: Pos } = first.kind === 'hash' ? { name: first.name, at: first.pos } : hashOp(first);
            closing();
            return { kind: 'hashop', op: 'count', name: of.name, pos: head.pos, at: of.at };
        }
        const array = next();
        // perl's `shift` alone shifts the program's arguments, or a sub's
        // (T152); its `scalar` takes any expression.
        if (array.kind !== 'array') return refuse(`${head.text} names an array, found ${show(array)}: ${head.text}(@a${name.shape === 'push' || name.shape === 'splice' ? ', ...' : ''})`, array.pos);
        const made = (args: readonly Expr[]): Expr => ({ kind: 'arrayop', op: head.text, name: array.name, args, pos: head.pos, at: array.pos });
        if (name.shape === 'push') {
            // perl warns of a `push` with nothing to add.
            if (peek().kind !== ',') refuse(`${head.text} needs a value to add: ${head.text} @${array.name}, ...`, peek().pos);
            next();
            if (!open) return made(list());
            const args = itemsTo(')');
            if (args.length === 0) refuse(`${head.text} needs a value to add: ${head.text} @${array.name}, ...`, head.pos);
            return made(args);
        }
        if (name.shape === 'splice') {
            if (peek().kind !== ',') {
                closing();
                return made([]);
            }
            next();
            return made(itemsTo(')'));
        }
        if (open) {
            closing();
            return made([]);
        }
        // `pop @a + 1` doesn't compile in perl, and `pop @a || 0` does
        // (T152): without its brackets, the array ends the expression.
        const after = peek();
        if (!(ends(after) || after.kind === ')' || after.kind === ',' || after.kind === ']' || after.kind === 'eof' || isModifier(after))) {
            refuse(`${head.text} @${array.name} before ${show(after)}: perl reads on for the array, or does not compile it; write ${head.text}(@${array.name})`, head.pos);
        }
        return made([]);
    };

    // The name of a variable that is being declared: not `$_`, which perl
    // does not let a program declare (`Can't use global $_ in "my"`).
    const own = (v: Token & { kind: 'var' }): string =>
        (v.name === '_' ? refuse('$_ is not a name a program may declare: it is what a for, a map or a grep gives its block', v.pos)
        : v.name === 'a' || v.name === 'b' ? refuse(`$${v.name} is not a name a program may declare: $a and $b are the two values a sort gives its block`, v.pos)
        : v.name);

    // `map { ... } LIST` and `grep { ... } LIST`, the word just read.
    const binder = (head: Token): Expr => {
        const open = next();
        if (open.kind === '(') refuse(`${head.text} takes no brackets of its own: ${head.text} { ... } LIST`, open.pos);
        if (open.kind !== '{') refuse(`${head.text} takes a block: ${head.text} { ... } LIST; with an expression and a comma it is not in the language (D85)`, open.pos);
        const { body, items } = blockAndList(head, true);
        return { kind: 'binder', op: head.text, var: { kind: 'my', name: '_', pos: head.pos }, body, items, pos: head.pos };
    };

    // `sort LIST` and `sort { ... } LIST`, the word just read (step 10c).
    const sort = (head: Token): Expr => {
        const first = peek();
        if (first.kind === '(') refuse('sort takes no brackets of its own: sort LIST, or sort { ... } LIST', first.pos);
        if (first.kind === '{') {
            next();
            const { body, items } = blockAndList(head, false);
            return { kind: 'sort', a: { kind: 'my', name: 'a', pos: head.pos }, b: { kind: 'my', name: 'b', pos: head.pos }, body, items, pos: head.pos };
        }
        // perl takes a word first after `sort` for the name of a sub that
        // compares, with its brackets too, and `true` there for a string
        // (T189, T29); and a scalar for a sub to call (D21).
        if (first.kind === 'word' && !PERL_KEYWORDS.includes(first.text)) {
            refuse(`${first.text} first after sort: perl takes a word there for the name of a sub that compares, or for a string; put a + before it, or give sort a block`, first.pos);
        }
        if (first.kind === 'var') refuse(`${first.text} first after sort: perl takes a scalar there for a sub that compares; put a + before it, or give sort a block`, first.pos);
        if (ends(first) || first.kind === ')' || first.kind === ']' || first.kind === ',' || first.kind === 'eof' || isModifier(first)) refuse('sort needs a list', first.pos);
        return { kind: 'sort', items: list(), pos: head.pos };
    };

    // The block of a `map`, a `grep` or a `sort`, its `{` just read, and
    // the list after it. `says`: the block may end in a `say`.
    const blockAndList = (head: Token, says: boolean): { body: Stmt[]; items: Expr[] } => {
        // perl guesses whether this is a block or an anonymous hash from
        // what comes first in it (T175, T192, D21): refused where its
        // guess is the hash.
        const first = peek();
        if (first.kind === '}') refuse(`an empty block after ${head.text}: an anonymous hash, to perl`, first.pos);
        if (first.kind === '{') refuse(`'{' first in ${head.text}'s block: an anonymous hash, to perl`, first.pos);
        if ((first.kind === 'str' || first.kind === 'int' || first.kind === 'num') && tokens[i + 1]?.kind === ',') {
            refuse(`${first.text} and a comma first in ${head.text}'s block: perl takes the block for an anonymous hash, and does not compile it; put the list in brackets`, first.pos);
        }
        const outer = inList;
        inList = false;
        depth += 1;
        blocks += 1;
        const body: Stmt[] = [];
        while (peek().kind !== '}' && peek().kind !== 'eof') body.push(statement());
        blocks -= 1;
        depth -= 1;
        inList = outer;
        const close = next();
        if (close.kind !== '}') unexpected(close, "'}'");
        // The block's value is its last statement's (T176).
        const last = body.at(-1);
        // And `true` after a `say` or a `print`, as a sub's is (D70).
        if (last?.kind !== 'do' && !(says && last?.kind === 'call')) refuse(`${head.text}'s block ends in an expression, which is its value`, (last ?? close).pos);
        const after = peek();
        if (after.kind === ',') refuse(`a comma after ${head.text}'s block: perl does not compile it`, after.pos);
        if (ends(after) || after.kind === ')' || after.kind === ']' || after.kind === 'eof' || isModifier(after)) refuse(`${head.text} needs a list after its block`, after.pos);
        return { body, items: list() };
    };

    // `join` and `reverse`, the word just read: a list in brackets, or to
    // the end of the list they stand in.
    const listOp = (head: Token): Expr => {
        let args: Expr[];
        if (peek().kind === '(') {
            next();
            args = itemsTo(')');
            // perl does not compile `reverse(@x)[0]` (T168's kin).
            if (peek().kind === '[') refuse(`'[' after ${head.text}(...): perl does not compile it; bracket the whole, (${head.text}(...))[...]`, peek().pos);
        } else {
            const t = peek();
            args = ends(t) || t.kind === ')' || t.kind === ']' || t.kind === ',' || t.kind === 'eof' || isModifier(t) ? [] : list();
        }
        // `die;` and `warn;` say `Died` and `Warning: something's wrong`
        // (T300, T314).
        const empty = head.text === 'die' || head.text === 'warn';
        if (args.length === 0 && !empty) refuse(head.text === 'join' ? 'join needs a separator: join(SEP, LIST)' : `${head.text} of nothing`, head.pos);
        const made: Expr = { kind: 'listop', op: head.text, args, pos: head.pos };
        if (empty) units.at(-1)?.push(made);
        return made;
    };

    // A call of one of the program's subs, its name just read and a
    // bracket next (D21). One comma may follow the last argument, as in
    // perl; two together are one to perl, which counts the arguments
    // either side as if nothing were wrong (T137).
    const invoke = (head: Token): Expr => {
        next();
        const outer = inList;
        inList = true;
        const args: Expr[] = [];
        while (peek().kind !== ')') {
            if (peek().kind === ',') refuse("a comma with no argument before it: perl leaves it out, in silence, where it doesn't refuse it", peek().pos);
            args.push(expression(COMMA_ROW));
            const t = peek();
            if (t.kind === 'op' && (infixOp(t.text)?.row ?? 0) > COMMA_ROW) {
                refuse(`'${t.text}' in a list of arguments takes the whole list for its left side, to perl: bracket what it joins`, t.pos);
            }
            if (t.kind !== ',') break;
            next();
        }
        inList = outer;
        closing();
        return { kind: 'invoke', name: head.text, args, pos: head.pos };
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
        if (t.kind === 'str' && t.pieces !== undefined) {
            // A string with a variable in it (step 11a): each piece the
            // node it is outside a string, the text between as strings.
            const index = (x: Index): Expr => {
                if (x.kind === 'var') return { kind: 'var', name: x.name, pos: x.pos };
                if (x.kind === 'range') return { kind: 'binary', op: '..', left: index(x.from), right: index(x.to), pos: x.pos };
                const whole: Expr = { kind: 'int', text: x.text, value: BigInt(x.text), pos: x.pos };
                return x.negative ? { kind: 'unary', op: '-', operand: whole, pos: x.pos } : whole;
            };
            const parts = t.pieces.map((p): Expr =>
                p.kind === 'text' ? { kind: 'str', text: '', value: p.value, pos: t.pos }
                : p.kind === 'elem' ? { kind: 'elem', name: p.name, index: index(p.index), pos: p.pos }
                : p.kind === 'helem' ? { kind: 'elem', name: p.name, hash: true, pos: p.pos,
                    index: p.key.kind === 'var' ? { kind: 'var', name: p.key.name, pos: p.key.pos } : { kind: 'str', text: p.key.text, value: p.key.text, pos: p.pos } }
                : p.kind === 'slice' ? { kind: 'slice', name: p.name, indexes: p.indexes.map(index), pos: p.pos }
                : { kind: p.kind, name: p.name, pos: p.pos });
            return { kind: 'interp', text: t.text, parts, pos: t.pos };
        }
        if (t.kind === 'str') {
            // `-word` before `=>` or alone in a hash's braces is the
            // string `-word`, to perl.
            const sign = tokens[i - 2];
            if (t.bare && sign?.kind === 'op' && prefixOp(sign.text)?.sign) {
                refuse(`'${sign.text}' before the word ${t.text}, which is a string here: perl makes one string of the two; write it in quotes`, sign.pos);
            }
            return { kind: 'str', text: t.text, value: t.value, pos: t.pos };
        }
        if (t.kind === 'hash') return { kind: 'array', name: t.name, hash: true, pos: t.pos };
        if (t.kind === '(') {
            // A list, if a comma stands in the brackets or nothing does;
            // otherwise an expression, grouped. And either may be sliced.
            const isList = peek().kind === ')' || commaAhead(i, ')');
            let inner: Expr;
            let items: readonly Expr[];
            if (isList) {
                items = itemsTo(')');
                inner = { kind: 'list', items, pos: t.pos, bracketed: true };
            } else {
                const one = bracketed();
                items = [one];
                inner = { ...one, bracketed: true };
            }
            if (peek().kind !== '[') return inner;
            const open = next();
            const indexes = itemsTo(']');
            if (indexes.length === 0) refuse('a slice with no index', open.pos);
            if (peek().kind === '[') refuse('an element of an element: an array of arrays is not in the language yet', peek().pos);
            return { kind: 'slice', items, indexes, pos: open.pos };
        }
        if (t.kind === 'array') {
            const brace = peek();
            if (brace.kind === '{' && brace.subscript) return hashSlice(t);
            if (brace.kind === '{') refuse(`a blank between @${t.name} and '{': a slice of a hash is written @${t.name}{...}`, brace.pos);
            if (peek().kind !== '[') return { kind: 'array', name: t.name, pos: t.pos };
            if (!touching(i - 1)) refuse(`a blank between @${t.name} and '[': a slice is written @${t.name}[...]`, peek().pos);
            const open = next();
            const indexes = itemsTo(']');
            // perl does not compile `@a[]`.
            if (indexes.length === 0) refuse('a slice with no index: perl refuses it', open.pos);
            if (peek().kind === '[') refuse('an element of an element: an array of arrays is not in the language yet', peek().pos);
            return { kind: 'slice', name: t.name, indexes, pos: t.pos };
        }
        if (t.kind === 'lastindex') return { kind: 'lastindex', name: t.name, pos: t.pos };
        // A variable, and `++` or `--` hard after it or not: they bind
        // tighter than anything else there is.
        if (t.kind === 'var') {
            const target = place(t);
            const after = peek();
            if (after.kind !== 'op' || !stepOp(after.text)) return target;
            next();
            return { kind: 'step', op: after.text, before: false, target, pos: after.pos };
        }
        if (t.kind === 'op' && stepOp(t.text)) {
            const v = next();
            if (v.kind !== 'var') return refuse(`'${t.text}' is for a variable: ${t.text}$x`, t.pos);
            return { kind: 'step', op: t.text, before: true, target: place(v), pos: t.pos };
        }
        const prefix = t.kind === 'op' ? prefixOp(t.text) : undefined;
        if (prefix) return prefixed(t, prefix.row);
        if (t.kind === 'word' && NAMES.get(t.text)?.kind === 'my') {
            const v = next();
            if (v.kind === 'array') return { kind: 'myarray', name: v.name, pos: t.pos };
            if (v.kind === 'hash') return { kind: 'myarray', name: v.name, hash: true, pos: t.pos };
            // `my ($x, undef, @rest)`: each a declaration, or a value to
            // skip.
            if (v.kind === '(') {
                const items: Expr[] = [];
                while (peek().kind !== ')') {
                    const d = next();
                    if (d.kind === 'var' && peek().kind !== '[' && peek().kind !== '{') items.push({ kind: 'my', name: own(d), pos: d.pos });
                    else if (d.kind === 'array') items.push({ kind: 'myarray', name: d.name, pos: d.pos });
                    else if (d.kind === 'hash') items.push({ kind: 'myarray', name: d.name, hash: true, pos: d.pos });
                    else if (d.kind === 'word' && d.text === 'undef') items.push({ kind: 'constant', name: 'undef', pos: d.pos });
                    else return refuse(`in my (...), expected a variable, an array, a hash or undef, found ${show(d)}`, d.pos);
                    if (peek().kind === ',') next();
                    else if (peek().kind !== ')') unexpected(peek(), "',' or ')'");
                }
                next();
                if (items.length === 0) refuse('my () declares nothing', v.pos);
                return { kind: 'list', items, my: true, pos: t.pos, bracketed: true };
            }
            if (v.kind !== 'var') return refuse(`after 'my', expected a variable, found ${show(v)}`, v.pos);
            return { kind: 'my', name: own(v), pos: t.pos };
        }
        const name = t.kind === 'word' ? NAMES.get(t.text) : undefined;
        if (name?.kind === 'constant' || name?.kind === 'unary' || name?.kind === 'function' || name?.kind === 'statement') return apply(t);
        if (name?.kind === 'arrayop') return arrayOp(t);
        if (name?.kind === 'hashop') return hashOp(t);
        if (name?.kind === 'listop') return listOp(t);
        if (name?.kind === 'binder') return binder(t);
        if (name?.kind === 'sort') return sort(t);
        // perl takes `$done and last` and `$x ? last : next` (T120), and
        // `my $x = return 5;` (T139).
        if (name?.kind === 'jump' || name?.kind === 'return') {
            return refuse(`${t.text} is a statement, not a value: write '${t.text} if ...;' or '${t.text} unless ...;'`, t.pos);
        }
        if (name?.kind === 'sub') return refuse('a sub with no name, as a value, is not in the language yet', t.pos);
        // perl refuses each of these where a value stands (T315, D143).
        if (name?.kind === 'try' || name?.kind === 'catch') return refuse(`${t.text} is a statement, not a value: perl does not compile it here`, t.pos);
        if (t.kind === 'op' && NAMES.get(t.text)?.kind === 'yada') return refuse("'...' is a statement alone, which dies: perl does not compile it anywhere else", t.pos);
        if (callable(t)) {
            if (peek().kind === '(') return invoke(t);
            return refuse(`'${t.text}' is not in the language; a call of a sub of the program's has brackets: ${t.text}(...)`, t.pos);
        }
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
                // A list assignment: brackets on the left, round a list of
                // targets or round one (`($x) = 5` is one to perl).
                // A slice on the left, of an array or of a hash, is a list
                // assignment's one target (D100).
                const slice = left.kind === 'slice' && left.name !== undefined;
                if (slice && t.text !== '=') refuse(`'${t.text}' on a slice: a slice is assigned with =`, t.pos);
                const single = slice || left.kind === 'var' || left.kind === 'my' || left.kind === 'elem' || left.kind === 'array' || left.kind === 'myarray';
                if (left.kind === 'list' || slice || (single && left.bracketed)) {
                    if (t.text !== '=') refuse(`'${t.text}' with a list on its left: a list is assigned with =`, t.pos);
                    // (One target in brackets is that target, its brackets
                    // the list's.)
                    const { bracketed: _, ...one } = left;
                    const targets: readonly Expr[] = left.kind === 'list' ? left.items : [one as Expr];
                    const value = expression(infix.row + 1);
                    left = left.kind === 'list' && left.my ? { kind: 'listassign', targets, my: true, value, pos: t.pos } : { kind: 'listassign', targets, value, pos: t.pos };
                    continue;
                }
                if (left.kind === 'array' || left.kind === 'myarray') {
                    // perl does not compile `@a += 1`.
                    if (t.text !== '=') refuse(`'${t.text}' on ${left.hash ? 'a hash: a hash' : 'an array: an array'} is assigned with =`, t.pos);
                    left = { kind: 'assign', op: t.text, target: left, value: expression(infix.row + 1), pos: t.pos };
                    continue;
                }
                if (left.kind !== 'var' && left.kind !== 'my' && left.kind !== 'elem') {
                    return refuse(`the left side of '${t.text}' is a variable, an element, an array, a hash, or a list of them in brackets`, t.pos);
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
            if (infix.range && peek().kind === 'op' && infixOp(peek().text)?.range) {
                refuse("'..' after a range: perl does not compile a range of a range", peek().pos);
            }
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
    const argument = (head: Token): Expr[] => {
        // The first word after `say`, behind any opening brackets, is a
        // file handle to perl when a blank follows it, unless perl has
        // already seen a sub of that name: `say f (1);` compiles after
        // `sub f` and not before (T136).
        let first = i;
        while (tokens[first]!.kind === '(') first += 1;
        if (callable(tokens[first]!) && tokens[first + 1]!.kind === '(' && !touching(first)) {
            const word = tokens[first]!.text;
            refuse(`a blank between ${word} and its bracket, first after ${head.text}: perl takes ${word} for a file handle unless it has seen the sub already; write ${word}(...)`, tokens[first + 1]!.pos);
        }
        const open = peek();
        // The word operators bind more loosely than `say` does: `say 0 or
        // 2;` is `(say 0) or 2` (T106). So without brackets the argument
        // stops before one, and the statement refuses it.
        // A list, where a comma stands among the arguments: each an item.
        if (open.kind !== '(') return commaAhead(i, ';') ? list() : [expression(AND_ROW)];
        next();
        // perl's `say()` prints `$_`.
        if (peek().kind === ')') refuse(`${head.text}() with nothing to print: perl prints $_`, open.pos);
        const isList = commaAhead(i, ')');
        const inner = isList ? itemsTo(')') : [{ ...bracketed(), bracketed: true as const }];
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
        // T100). The lexer has looked as perl does. What may follow is
        // the semicolon or a modifier, and perl wants either on the line
        // the brackets are on (T128); anything else is refused for what
        // it is, below.
        if (head.kind === 'word' && head.asFunction && (ends(after) || isModifier(after))) {
            refuse(`${head.text} (...) after one blank: perl warns unless the brackets close on this line, one in a string counting too, with ${show(after)} after them: write ${head.text}(...)`, open.pos);
        }
        return inner;
    };

    // A word operator after a statement's expression: `$x = 1 and $y =
    // 2;` is two assignments joined, to perl, and a statement here is
    // one (D56).
    const loose = (): void => {
        const after = peek();
        // `$done and last;`: the commonest of them, and the answer is an
        // `if` (T120).
        const then = tokens[i + 1];
        const thenKind = then?.kind === 'word' ? NAMES.get(then.text)?.kind : undefined;
        if (after.kind === 'op' && infixOp(after.text) && then !== undefined && (thenKind === 'jump' || thenKind === 'return')) {
            refuse(`${then.text} is a statement, not a value: write '${then.text} if ...;' or '${then.text} unless ...;'`, then.pos);
        }
        // `$x or die ...;` (D146): `die ... unless $x;` says it.
        if (after.kind === 'op' && infixOp(after.text) && then?.kind === 'word' && then.text === 'die') {
            refuse(`'${after.text} die' after a statement: a statement is not joined by a word operator here (D56); write die ... ${after.text === 'or' ? 'unless' : 'if'} ...;`, after.pos);
        }
        if (after.kind === 'op' && infixOp(after.text)) {
            refuse(`'${after.text}' after a statement joins it to what follows, to perl, which binds '${after.text}' more loosely than '=': write it as an if`, after.pos);
        }
        // `my @a = 1, 2, 3;` is `(my @a = 1), 2, 3` to perl: one element,
        // and a warning for each of the rest (T168).
        if (after.kind === ',') {
            // `map { $_ => 1 } @l`: a hash and no block, to perl, by a
            // guess (T175).
            if (blocks > 0) refuse("a comma in the block of a map, a grep or a sort: put the list in brackets, map { ($_ => 1) } ...", after.pos);
            refuse("a comma after an assignment's right side: perl takes the assignment for the first item of a list; put the list in brackets", after.pos);
        }
    };

    // `{ statements }`, the opening brace next.
    const block = (): Stmt[] => {
        const open = next();
        if (open.kind !== '{') unexpected(open, "'{'");
        depth += 1;
        const body: Stmt[] = [];
        while (peek().kind !== '}' && peek().kind !== 'eof') body.push(statement());
        depth -= 1;
        const close = next();
        if (close.kind !== '}') unexpected(close, "'}'");
        return body;
    };

    // `(test)` and a block, for `if`, `elsif` and `unless`.
    const arm = (head: Token, negate: boolean): Arm => {
        const open = next();
        if (open.kind !== '(') unexpected(open, `'(' after ${head.text}`);
        const test = unit(head.pos, bracketed);
        return negate ? { test, negate, body: block(), pos: head.pos } : { test, body: block(), pos: head.pos };
    };

    // `say`, `print`, or an expression that is a statement, as far as its
    // semicolon or a modifier.
    const simple = (): Stmt => {
        const head = peek();
        const name = head.kind === 'word' ? NAMES.get(head.text) : undefined;
        if (head.kind === 'word' && name === undefined && !(callable(head) && tokens[i + 1]!.kind === '(')) {
            return refuse(callable(head) ? `'${head.text}' is not in the language; a call of a sub of the program's has brackets: ${head.text}(...)`
                : `'${head.text}' is not in the language`, head.pos);
        }
        // `return;` and `return VALUE;` (D72). What follows the value may
        // be a modifier, and no operator: `return $v or 9;` is `(return
        // $v) or 9` to perl, which warns (T139).
        if (name?.kind === 'return') {
            next();
            if (!inSub) refuse("return outside a sub: perl dies there, when it gets to it", head.pos);
            // perl's `return` in a `map` block ends the sub, and in a
            // `sort` block the comparison (T174).
            if (blocks > 0) refuse('return in the block of a map, a grep or a sort: perl ends the sub from the first two and the comparison from the third', head.pos);
            if (ends(peek()) || isModifier(peek())) return { kind: 'return', pos: head.pos };
            const value = expression(AND_ROW);
            const after = peek();
            if (after.kind === ',') refuse('a list after return is in brackets: return (..., ...);', after.pos);
            if (after.kind === 'op' && infixOp(after.text)) {
                refuse(`'${after.text}' after return's value: it binds more loosely than return does, and perl warns of it; bracket the value, return (... ${after.text} ...)`, after.pos);
            }
            return { kind: 'return', value, pos: head.pos };
        }
        if (name?.kind === 'statement') {
            next();
            // `say STDERR LIST;` (15b): the one file handle, a blank, and
            // a list that is not in brackets of its own.
            const handle = peek();
            const stderr = handle.kind === 'word' && NAMES.get(handle.text)?.kind === 'handle';
            if (stderr) {
                next();
                const after = peek();
                if (ends(after) || isModifier(after)) refuse(`${head.text} ${handle.text} with nothing to print: perl prints $_`, after.pos);
                if (after.kind === '(') refuse(`${head.text} ${handle.text} (...): write the list without brackets of its own, ${head.text} ${handle.text} ...;`, after.pos);
                if (touching(i - 2)) refuse(`${head.text}${handle.text}: a blank between ${head.text} and ${handle.text}`, handle.pos);
            }
            const args = argument(head);
            const after = peek();
            if (after.kind === ',') refuse(`',' after ${head.text}'s argument: a list is not in the language yet`, after.pos);
            if (after.kind === 'op' && infixOp(after.text)) {
                refuse(`'${after.text}' after ${head.text}'s argument: it binds more loosely than ${head.text} does, and joins what ${head.text} returns, to perl; bracket the argument, ${head.text}(... ${after.text} ...)`, after.pos);
            }
            return stderr ? { kind: 'call', name: head.text, args, stderr: true, pos: head.pos } : { kind: 'call', name: head.text, args, pos: head.pos };
        }
        if (name?.kind === 'elsif' || name?.kind === 'else') return refuse(`${head.text} without an if before it`, head.pos);
        // `last;`, `next NAME;`, and nothing else after either but an
        // `if` or `unless`: to perl what follows is an expression that
        // names a label, and `last + 1;` dies looking for a loop called
        // 1 (T120).
        if (name?.kind === 'jump') {
            next();
            const word = peek();
            const label: Label | undefined = word.kind === 'word' && isLabel(word.text) ? { name: next().text, pos: word.pos } : undefined;
            const after = peek();
            if (!ends(after) && !(after.kind === 'word' && NAMES.get(after.text)?.kind === 'if')) {
                refuse(`after '${head.text}' comes ';', a label in capitals, or an if or unless: perl takes anything else for an expression that names a label`, after.pos);
            }
            return label === undefined ? { kind: 'jump', name: head.text, pos: head.pos } : { kind: 'jump', name: head.text, label, pos: head.pos };
        }
        if (head.kind === ';' || head.kind === '}' || head.kind === ')' || head.kind === 'eof') return unexpected(next(), 'a statement');
        // In the block of a `map` or a `grep` the last statement is the
        // block's value, and may be two joined by a word operator (`$a
        // <=> $b or $a cmp $b`); one that is not the last only has a
        // value, and the checker refuses it.
        const expr = expression(blocks > 0 ? Infinity : AND_ROW);
        loose();
        return { kind: 'do', expr, pos: head.pos };
    };

    // The expressions of the first or the third part of a `for`, with
    // commas between them (D60), as far as `end`.
    const part = (end: ';' | ')'): Expr[] => {
        const items: Expr[] = [];
        while (peek().kind !== end) {
            if (items.length > 0) {
                const comma = next();
                if (comma.kind !== ',') unexpected(comma, `',' or '${end}'`);
            }
            items.push(expression(COMMA_ROW));
            const after = peek();
            if (after.kind === 'op' && infixOp(after.text)) {
                refuse(`'${after.text}' in a part of a for joins the parts on either side of it, to perl: bracket what it joins`, after.pos);
            }
        }
        next();
        return items;
    };

    // `while (T) { }`, `until (T) { }` and `for (F; T; E) { }`, the word
    // next, under a label or not.
    const loop = (label: Label | undefined): Stmt => {
        const head = next();
        const name = NAMES.get(head.text);
        const open = next();
        // `for my $x (LIST) { }`, a loop over a list (step 9b).
        if (name?.kind === 'for' && open.kind === 'word' && NAMES.get(open.text)?.kind === 'my') {
            const v = next();
            if (v.kind === '(') refuse(`${head.text} my (...) takes a list several values at a time, which is not in the language`, v.pos);
            if (v.kind !== 'var') return refuse(`after '${head.text} my', expected a variable, found ${show(v)}`, v.pos);
            const paren = next();
            if (paren.kind !== '(') unexpected(paren, `'(' after ${head.text} my $${v.name}`);
            // perl does not compile it (T155).
            if (peek().kind === ')') refuse(`${head.text} my $${v.name} () is a loop over nothing, and perl does not compile it`, paren.pos);
            const items = unit(head.pos, () => itemsTo(')'));
            const body = block();
            return { kind: 'foreach', var: { kind: 'my', name: own(v), pos: open.pos }, items, body, pos: head.pos, ...(label ? { label } : {}) };
        }
        if (open.kind !== '(') {
            // perl makes a variable from outside the loop's own while it
            // runs, and gives it back after.
            if (name?.kind === 'for' && open.kind === 'var') refuse(`${head.text} $${open.name} (...) borrows a variable from outside the loop: ${head.text} my $${open.name} (...)`, open.pos);
            unexpected(open, `'(' after ${head.text}`);
        }
        if (name?.kind === 'while') {
            // `while ()` is `while (1)` to perl, and `until ()` nothing (T123).
            if (peek().kind === ')' && !name.until) refuse("while () is while (1), to perl: say that, or for (;;)", open.pos);
            const test = unit(head.pos, bracketed, true);
            const body = block();
            return { kind: 'while', test, body, pos: head.pos, ...(name.until ? { negate: true as const } : {}), ...(label ? { label } : {}) };
        }
        // A `for` with no `;` in its brackets is a loop over a list.
        // (A `;` in the block of a `map` or a `grep` in a part is the
        // block's.)
        let depth = 0;
        let braces = 0;
        let semicolons = 0;
        for (let j = i; tokens[j]!.kind !== 'eof' && depth >= 0; j++) {
            const kind = tokens[j]!.kind;
            depth += kind === '(' ? 1 : kind === ')' ? -1 : 0;
            braces += kind === '{' ? 1 : kind === '}' ? -1 : 0;
            if (kind === ';' && depth === 0 && braces === 0) semicolons += 1;
        }
        if (semicolons === 0) {
            // `for (LIST) { }`: a loop over a list, with `$_` (step 10b).
            if (peek().kind === ')') refuse(`${head.text} () is a loop over nothing, and perl does not compile it`, open.pos);
            const items = unit(head.pos, () => itemsTo(')'));
            const body = block();
            return { kind: 'foreach', var: { kind: 'my', name: '_', pos: head.pos }, items, body, pos: head.pos, ...(label ? { label } : {}) };
        }
        // To perl `foreach` is `for`, with three parts too (T122).
        if (name?.kind === 'for' && name.each) refuse('foreach is the loop over a list here, foreach my $x (...): the loop of three parts is spelled for', head.pos);
        const [first, test, each] = unit(head.pos, (): [Expr[], Expr | undefined, Expr[]] => {
            const first = part(';');
            let test: Expr | undefined;
            if (peek().kind !== ';') test = expression(Infinity);
            semicolon();
            return [first, test, part(')')];
        });
        const body = block();
        return { kind: 'for', first, each, body, pos: head.pos, ...(test ? { test } : {}), ...(label ? { label } : {}) };
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
        // `no warnings 'recursion';` (D67): the pragma named `no warnings`.
        if (name?.kind === 'no') {
            next();
            const what = next();
            const pragma = `no ${what.text}`;
            if (what.kind !== 'word' || !PRAGMAS.has(pragma)) return refuse(`'${pragma}' is not in the language`, what.pos);
            const args = peek().kind === ';' ? [] : list();
            semicolon();
            return { kind: 'pragma', name: pragma, args, pos: head.pos };
        }
        // `sub NAME(PARAMETERS) { ... }` (D72). perl ties a named sub in a
        // loop or a sub to the first time round (T31).
        if (name?.kind === 'sub') {
            next();
            if (depth > 0) refuse('a sub stands at the top level of the file: not in a block, a loop or another sub', head.pos);
            const named = next();
            if (named.kind !== 'word' && named.kind !== 'version') return refuse(`after 'sub' comes a name, found ${show(named)}: a sub with no name is not in the language yet`, named.pos);
            // perl ignores a sub named for one of its own words, or doesn't
            // compile the call (T28); it reads `v1_0` as a version string
            // where it hasn't seen the sub yet (T136); and it stops at a
            // name too long. Here, so that the definition is what is
            // refused, and not the first call of it.
            if (NAMES.has(named.text) || PERL_WORDS.has(named.text)) refuse(`a sub may not be called ${named.text}: perl has a meaning of its own for the word`, named.pos);
            if (named.kind === 'version' || isVersionString(named.text)) {
                refuse(`a sub may not be called ${named.text}: perl reads v and digits as a version, where it has not yet seen the sub`, named.pos);
            }
            if (named.text.length > NAME_MAX_LENGTH) refuse(`a name of more than ${NAME_MAX_LENGTH} characters: perl refuses it as too long`, named.pos);
            // A sub with no signature takes any number of arguments and
            // sees none (D105): to perl they are in @_, which is not in the
            // language. That is `sub f(@)`, a slurpy parameter with no name.
            const bare = peek().kind === '{';
            const open = bare ? peek() : next();
            if (!bare && open.kind !== '(') return refuse(`after sub ${named.text} comes its signature, sub ${named.text}(...) { ... }, or its block, found ${show(open)}`, open.pos);
            const params: Param[] = bare ? [{ slurpy: true, pos: open.pos }] : [];
            while (!bare && peek().kind !== ')') {
                const v = next();
                // A slurpy parameter, `@rest` or `@`: the last, and with
                // no default; perl compiles neither otherwise (T182).
                if (v.kind === 'array') {
                    const after = peek();
                    if (after.kind === 'op' && (after.text === '=' || after.text === '//=' || after.text === '||=')) refuse('a slurpy parameter has no default: perl refuses one', after.pos);
                    if (after.kind !== ')') refuse(`${v.text} takes every argument that is left, so it is the last parameter: perl refuses one after it`, after.pos);
                    params.push(v.name === '' ? { slurpy: true, pos: v.pos } : { slurpy: true, rest: { kind: 'myarray', name: v.name, pos: v.pos }, pos: v.pos });
                    continue;
                }
                // A last parameter that is a hash, `%opts` or `%` alone
                // (step 12b). tree-sitter-perl takes `:$x`, and perl
                // doesn't (T55).
                if (v.kind === 'hash') {
                    const after = peek();
                    if (after.kind === 'op' && (after.text === '=' || after.text === '//=' || after.text === '||=')) refuse('a slurpy parameter has no default: perl refuses one', after.pos);
                    if (after.kind !== ')') refuse(`${v.text} takes every argument that is left, so it is the last parameter: perl refuses one after it`, after.pos);
                    params.push(v.name === '' ? { slurpy: true, hash: true, pos: v.pos } : { slurpy: true, hash: true, rest: { kind: 'myarray', name: v.name, hash: true, pos: v.pos }, pos: v.pos });
                    continue;
                }
                if (v.kind !== 'var') return refuse(`a parameter is $name or, last, @name, found ${show(v)}`, v.pos);
                const assign = peek();
                let param: Param = v.name === '' ? { pos: v.pos } : { my: { kind: 'my', name: own(v), pos: v.pos }, pos: v.pos };
                if (assign.kind === 'op' && (assign.text === '=' || assign.text === '//=' || assign.text === '||=')) {
                    next();
                    param = { ...param, op: assign.text };
                    if (peek().kind !== ',' && peek().kind !== ')') {
                        const outer = inList;
                        inList = true;
                        param = { ...param, default: unit(v.pos, () => expression(COMMA_ROW)) };
                        inList = outer;
                    } else if (v.name !== '') {
                        refuse(`'${assign.text}' with no default after it: perl refuses it`, assign.pos);
                    }
                } else if (assign.kind === 'op') {
                    refuse(`'${assign.text}' in a signature: a default is given with =, //= or ||=`, assign.pos);
                }
                params.push(param);
                const after = peek();
                if (after.kind === ',') {
                    next();
                    if (peek().kind === ',') refuse('two commas together in a signature', peek().pos);
                } else if (after.kind !== ')') {
                    unexpected(after, "',' or ')'");
                }
            }
            if (!bare) next();
            inSub = true;
            const body = block();
            inSub = false;
            return { kind: 'sub', name: named.text, params, body, pos: head.pos, named: named.pos, end: tokens[i - 1]!.pos };
        }
        // A block. An empty one is an anonymous hash to perl, `{}`, and a
        // statement that is only a value (T116).
        if (head.kind === '{') {
            const body = block();
            if (body.length === 0) refuse("an empty block is an anonymous hash, to perl: put a statement in it, or take it out", head.pos);
            return { kind: 'block', body, pos: head.pos };
        }
        // A label, `NAME:`, and the loop it is on (D61).
        if (head.kind === 'word' && name === undefined && tokens[i + 1]?.kind === ':') {
            next();
            const colon = next();
            if (!isLabel(head.text)) refuse(`a label is written in capitals: ${head.text.toUpperCase()}:`, head.pos);
            if (colon.pos.line !== head.pos.line || colon.pos.col !== head.pos.col + head.text.length) {
                refuse(`a label is hard against its colon: ${head.text}:`, colon.pos);
            }
            const word = peek();
            const kind = word.kind === 'word' ? NAMES.get(word.text)?.kind : undefined;
            if (kind !== 'while' && kind !== 'for') {
                refuse(`a label is on a loop: after ${head.text}: comes while, until or for`, word.pos);
            }
            return loop({ name: head.text, pos: head.pos });
        }
        if (name?.kind === 'while' || name?.kind === 'for') return loop(undefined);
        // `try { } catch ($e) { }` (step 15; D143). perl wants the catch
        // and its variable (T53), takes one catch, and warns of `finally`
        // (T313, D144).
        if (name?.kind === 'try') {
            next();
            if (peek().kind !== '{') unexpected(peek(), "'{' after try");
            const body = block();
            const word = peek();
            if (word.kind !== 'word' || NAMES.get(word.text)?.kind !== 'catch') return refuse('a try has a catch after its block: perl refuses it without one', word.pos);
            next();
            const open = next();
            if (open.kind !== '(') return refuse(`catch is followed by its variable in brackets, catch ($e): perl refuses it without (T53)`, open.pos);
            const v = next();
            if (v.kind !== 'var' || v.name === '') return refuse(`the variable of a catch is a scalar, catch ($e), found ${show(v)}`, v.pos);
            if (peek().kind === '[' || peek().kind === '{') unexpected(peek(), "')'");
            const shut = next();
            if (shut.kind !== ')') unexpected(shut, "')'");
            if (peek().kind !== '{') unexpected(peek(), "'{' after catch (...)");
            const handler = block();
            const more = peek();
            if (more.kind === 'word' && NAMES.get(more.text)?.kind === 'catch') refuse('a second catch: perl takes one', more.pos);
            if (more.kind === 'word' && more.text === 'finally') refuse('finally: perl 5.42 warns that it is experimental, and it is not in the language (D144)', more.pos);
            return { kind: 'try', body, var: { kind: 'my', name: own(v), pos: v.pos }, handler, pos: head.pos };
        }
        if (name?.kind === 'catch') return refuse('catch without a try before it', head.pos);
        // `...` (D145): a statement alone, and perl takes no modifier
        // after it (T315).
        if (head.kind === 'op' && NAMES.get(head.text)?.kind === 'yada') {
            next();
            const after = peek();
            if (!ends(after)) return refuse("'...' is a statement alone: perl does not compile anything after it but ';'", after.pos);
            ending();
            return { kind: 'do', expr: { kind: 'listop', op: 'die', args: [{ kind: 'str', text: '"Unimplemented"', value: 'Unimplemented', pos: head.pos }], pos: head.pos }, pos: head.pos };
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
        return unit(head.pos, () => modified(head));
    };

    // A statement that is not a block, a loop, an `if` or a `try`, and
    // the modifier after it if it has one.
    const modified = (head: Token): Stmt => {
        const inner = simple();
        // `STATEMENT if TEST;`, `unless`, `while`, `until`
        const word = peek();
        const modifier = word.kind === 'word' ? NAMES.get(word.text) : undefined;
        if (modifier?.kind !== 'if' && modifier?.kind !== 'while' && modifier?.kind !== 'for') {
            ending();
            return inner;
        }
        next();
        if (modifier.kind === 'for') {
            // `STATEMENT for LIST;` (step 10b). perl's `last for 1, 2;`
            // leaves the modifier's own loop (T191).
            if (inner.kind === 'return' || inner.kind === 'jump') refuse(`${inner.kind === 'return' ? 'return' : inner.name} ${word.text}: under a ${word.text} it would leave the ${word.text}'s own loop, to perl; write the loop with a block`, word.pos);
            const items = list();
            if (isModifier(peek())) refuse(`a second modifier after ${word.text}'s list: perl does not compile it`, peek().pos);
            ending();
            return { kind: 'foreach', var: { kind: 'my', name: '_', pos: word.pos }, items, body: [inner], modifier: true, pos: inner.pos };
        }
        if (inner.kind === 'return' && modifier.kind === 'while') {
            refuse(`return ${word.text}: a return takes an if or an unless`, word.pos);
        }
        const test = expression(Infinity);
        ending();
        if (modifier.kind === 'while') {
            return modifier.until ? { kind: 'while', test, negate: true, body: [inner], modifier: true, pos: inner.pos }
                : { kind: 'while', test, body: [inner], modifier: true, pos: inner.pos };
        }
        const one: Arm = modifier.unless ? { test, negate: true, body: [inner], pos: word.pos } : { test, body: [inner], pos: word.pos };
        return { kind: 'if', arms: [one], modifier: true, pos: inner.pos };
    };

    const body: Stmt[] = [];
    while (peek().kind !== 'eof') body.push(statement());
    return { kind: 'program', body, end: peek().pos };
};
