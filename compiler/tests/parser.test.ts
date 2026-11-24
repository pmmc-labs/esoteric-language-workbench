import { test } from 'node:test';
import assert from 'node:assert/strict';
import { lex } from '../src/lexer.ts';
import { parse } from '../src/parser.ts';
import { CompileError } from '../src/errors.ts';
import type { Expr } from '../src/ast.ts';

const refused = (src: string, message: string, line: number, col: number) =>
    assert.throws(() => parse(lex(src)), (e: unknown) => {
        assert.ok(e instanceof CompileError, String(e));
        assert.deepEqual([e.message, e.line, e.col], [message, line, col]);
        return true;
    });

// An expression's grouping, every operator's operands in brackets, and a
// star where the source had brackets of its own.
const shape = (e: Expr): string => {
    const s = e.kind === 'int' || e.kind === 'num' ? e.text
        : e.kind === 'unary' ? `(${e.op}${shape(e.operand)})`
        : `(${shape(e.left)} ${e.op} ${shape(e.right)})`;
    return e.bracketed ? s + '*' : s;
};
const argument = (src: string): Expr => {
    const stmt = parse(lex(src)).body[0]!;
    assert.equal(stmt.kind, 'call');
    return stmt.kind === 'call' ? stmt.args[0]! : assert.fail();
};
const grouped = (src: string) => shape(argument(src));

test('the tree, with positions', () => {
    assert.deepEqual(parse(lex('use v5.42;\n  say 010;\n')), {
        kind: 'program',
        body: [
            { kind: 'use', version: 'v5.42', pos: { line: 1, col: 1 } },
            { kind: 'call', name: 'say', pos: { line: 2, col: 3 }, args: [
                { kind: 'int', text: '010', value: 10n, pos: { line: 2, col: 7 } },
            ] },
        ],
        end: { line: 3, col: 1 },
    });
    assert.deepEqual(parse(lex(' ')), { kind: 'program', body: [], end: { line: 1, col: 2 } });
});

test('an operator node is at its operator', () => {
    assert.deepEqual(argument('say 1 +\n -2;'), {
        kind: 'binary', op: '+', pos: { line: 1, col: 7 },
        left: { kind: 'int', text: '1', value: 1n, pos: { line: 1, col: 5 } },
        right: { kind: 'unary', op: '-', pos: { line: 2, col: 2 },
            operand: { kind: 'int', text: '2', value: 2n, pos: { line: 2, col: 3 } } },
    });
});

// What perl makes of each is in t/030-precedence.pl, which perl checks.
test("precedence and associativity are perlop's", () => {
    assert.equal(grouped('say 2 - 3 - 4;'), '((2 - 3) - 4)');
    assert.equal(grouped('say 2 + 3 * 4;'), '(2 + (3 * 4))');
    assert.equal(grouped('say 2 * 3 + 4;'), '((2 * 3) + 4)');
    assert.equal(grouped('say 7 % 3 * 2;'), '((7 % 3) * 2)');
    assert.equal(grouped('say 2 * 7 % 3;'), '((2 * 7) % 3)');
    assert.equal(grouped('say 10 - 7 % 3 + 1;'), '((10 - (7 % 3)) + 1)');
    assert.equal(grouped('say -2 * -3;'), '((-2) * (-3))');
    assert.equal(grouped('say - 7 % 3;'), '((-7) % 3)');
    assert.equal(grouped('say - - 5;'), '(-(-5))');
    assert.equal(grouped('say +-+-5;'), '(+(-(+(-5))))');
    assert.equal(grouped('say 1 - - - 2;'), '(1 - (-(-2)))');
});

// What perl makes of each is in t/081-num-precedence.pl, which perl checks.
test('** binds tighter than a sign before it, and groups from the right', () => {
    assert.equal(grouped('say -2 ** 2;'), '(-(2 ** 2))');
    assert.equal(grouped('say 2 ** 3 ** 2;'), '(2 ** (3 ** 2))');
    assert.equal(grouped('say 2 ** -1;'), '(2 ** (-1))');
    assert.equal(grouped('say 2 ** -2 ** 2;'), '(2 ** (-(2 ** 2)))');
    assert.equal(grouped('say - 2 ** - 2;'), '(-(2 ** (-2)))');
    assert.equal(grouped('say 2 * 3 ** 2;'), '(2 * (3 ** 2))');
    assert.equal(grouped('say 2 ** 3 * 2;'), '((2 ** 3) * 2)');
    assert.equal(grouped('say 4 / 2 * 3;'), '((4 / 2) * 3)');
    assert.equal(grouped('say 7 / 2 % 2;'), '((7 / 2) % 2)');
    assert.equal(grouped('say 1 - 2 / 4;'), '(1 - (2 / 4))');
});

test('what a literal is worth', () => {
    const worth = (src: string) => { const e = argument(src); return e.kind === 'int' || e.kind === 'num' ? `${e.kind} ${e.value}` : assert.fail(); };
    assert.equal(worth('say 1_000;'), 'int 1000');
    assert.equal(worth('say 0x1F;'), 'int 31');
    assert.equal(worth('say 0XfF;'), 'int 255');
    assert.equal(worth('say 0b1_01;'), 'int 5');
    assert.equal(worth('say 0O17;'), 'int 15');
    assert.equal(worth('say 9223372036854775808;'), 'int 9223372036854775808');
    assert.equal(worth('say 1.5;'), 'num 1.5');
    assert.equal(worth('say .5_5;'), 'num 0.55');
    assert.equal(worth('say 1e1_0;'), 'num 10000000000');
    assert.equal(worth('say 1.5E-3;'), 'num 0.0015');
    assert.equal(worth('say 1e400;'), 'num Infinity');
    assert.equal(worth('say 0.1;'), 'num 0.1');
});

test('brackets group, and are remembered', () => {
    assert.equal(grouped('say 2 * (3 + 4);'), '(2 * (3 + 4)*)');
    assert.equal(grouped('say -(7 % 3);'), '(-(7 % 3)*)');
    assert.equal(grouped('say +(1 + 2) * 3;'), '((+(1 + 2)*) * 3)');
    assert.equal(grouped('say 1 - ((2));'), '(1 - 2*)');
    assert.equal(grouped('say(1 + 2);'), '(1 + 2)*');
    assert.equal(grouped('say((1 + 2) * 3);'), '((1 + 2)* * 3)*');
    assert.equal(grouped('say (5);'), '5*');
    assert.equal(grouped('say\n(5)\n;'), '5*');
});

test('what a statement may start with', () => {
    refused('use v5.42;\n;', "expected a statement, found ';'", 2, 1);
    refused('42;', 'expected a statement, found 42', 1, 1);
    refused('v5.42;', 'expected a statement, found v5.42', 1, 1);
    refused('(1);', "expected a statement, found '('", 1, 1);
    refused('- 1;', "expected a statement, found '-'", 1, 1);
    refused('use v5.42;\nprint 42;', "'print' is not in the language", 2, 1);
    refused('say42;', "'say42' is not in the language", 1, 1);
});

test('use takes a version', () => {
    refused('use strict;', "after 'use', expected a version, found 'strict'", 1, 5);
    refused('use 5;', "after 'use', expected a version, found 5", 1, 5);
    refused('use', "after 'use', expected a version, found the end of the file", 1, 4);
    refused('use v5.42 say 1;', "expected ';', found 'say'", 1, 11);
});

test('where an operand is wanted', () => {
    const wanted = (found: string) => `expected a number or '(', found ${found}`;
    refused('say;', wanted("';'"), 1, 4);
    refused('say 1 + ;', wanted("';'"), 1, 9);
    refused('say 1 +', wanted('the end of the file'), 1, 8);
    refused('say -;', wanted("';'"), 1, 6);
    refused('say ();', wanted("')'"), 1, 6);
    refused('say (+);', wanted("')'"), 1, 7);
    refused('say say 1;', wanted("'say'"), 1, 5);
    refused('say v5.42;', wanted('v5.42'), 1, 5);
    // perl has a glob `*3` and a hash `%2` here.
    refused('say 2 * *3;', wanted("'*'"), 1, 9);
    refused('say * 2;', wanted("'*'"), 1, 5);
    refused('say % 2;', wanted("'%'"), 1, 5);
    refused('say 1 % % 2;', wanted("'%'"), 1, 9);
});

test('where an operator or an end is wanted', () => {
    refused('say 1 2;', "expected ';', found 2", 1, 7);
    refused('say 1.5 .5;', "expected ';', found .5", 1, 9);
    refused('say 1 (2);', "expected ';', found '('", 1, 7);
    refused('say(1 + 2;', "expected ')', found ';'", 1, 10);
    refused('say 1 + 2);', "expected ';', found ')'", 1, 10);
    refused('say (1) (2);', "expected ';', found '('", 1, 9);
    refused('say 1 + (2 3);', "expected ')', found 3", 1, 12);
    // One of perl's operators that is a word.
    refused('say 4 x 2;', "'x' is not in the language yet", 1, 7);
    refused('say 1 and 2;', "'and' is not in the language yet", 1, 7);
    refused('say not 1;', "'not' is not in the language yet", 1, 5);
    refused('say 1 foo 2;', "expected ';', found 'foo'", 1, 7);
});

test("an operator after say's brackets (T25)", () => {
    const message = (op: string) => `'${op}' after say (...): perl takes the brackets for all of say's arguments; bracket the whole expression`;
    refused('say (1 + 2) * 3;', message('*'), 1, 13);
    refused('say(1 + 2) * 3;', message('*'), 1, 12);
    refused('say ((1 + 2)) - 3;', message('-'), 1, 15);
    refused('say (1) + 2;', message('+'), 1, 9);
    refused('say\n(1)\n% 2;', message('%'), 3, 1);
});

test('say, one blank, and a bracket: all on one line (T76)', () => {
    const message = "say (...) after one blank must end on the same line, ';' and all, or perl warns: write say(...)";
    refused('say (1 +\n2);', message, 1, 5);
    refused('say (1 + 2)\n;', message, 1, 5);
    refused('say (1 + 2) # then\n;', message, 1, 5);
    refused('say (\n1);', message, 1, 5);
    refused('use v5.42;\n  say\t(1)\n;', message, 2, 7);
    assert.equal(grouped('say (1 + 2) ;'), '(1 + 2)*');
    assert.equal(grouped('say (1 + 2); # after'), '(1 + 2)*');
    // perl doesn't look after two blanks, a newline, or none.
    assert.equal(grouped('say  (1 +\n2)\n;'), '(1 + 2)*');
    assert.equal(grouped('say\n(1 +\n2)\n;'), '(1 + 2)*');
    assert.equal(grouped('say(1 +\n2)\n;'), '(1 + 2)*');
});

test('every statement ends with its semicolon, and only one', () => {
    refused('use v5.42;\nsay 1', "expected ';', found the end of the file", 2, 6);
    refused('say 1\nsay 2;', "expected ';', found 'say'", 2, 1);
    refused('say 1;;', "expected a statement, found ';'", 1, 7);
});
