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
    const s = e.kind === 'int' || e.kind === 'num' || e.kind === 'str' ? e.text
        : e.kind === 'unary' ? `(${e.op}${shape(e.operand)})`
        : e.kind === 'apply' ? `${e.name}[${e.args.map(shape).join(', ')}]`
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
    refused('use v5.42;\nprintf 42;', "'printf' is not in the language", 2, 1);
    refused('say42;', "'say42' is not in the language", 1, 1);
    // perl warns of a useless use in void context.
    refused('length "abc";', 'length has a value, and nothing is done with it here', 1, 1);
    refused('substr("abc", 1);', 'substr has a value, and nothing is done with it here', 1, 1);
    refused('"abc";', 'expected a statement, found "abc"', 1, 1);
});

// What perl makes of each is in t/173-named-unary.pl and
// t/174-dot-and-x.pl, which perl checks.
test("the dot is at the level of + and -, and x at the level of * (perlop)", () => {
    assert.equal(grouped('say 1 . 2 + 3;'), '((1 . 2) + 3)');
    assert.equal(grouped('say 1 + 2 . 3;'), '((1 + 2) . 3)');
    assert.equal(grouped('say 1 . 2 * 3;'), '(1 . (2 * 3))');
    assert.equal(grouped('say "a" x 2 x 3;'), '(("a" x 2) x 3)');
    assert.equal(grouped('say "a" . "b" x 2;'), '("a" . ("b" x 2))');
    assert.equal(grouped('say 2 * 3 x 2;'), '((2 * 3) x 2)');
    assert.equal(grouped('say 2 x 3 + 2;'), '((2 x 3) + 2)');
    assert.equal(grouped('say -"2" x 2;'), '((-"2") x 2)');
    assert.equal(grouped('say 2 x 2 ** 2;'), '(2 x (2 ** 2))');
});

test('a named unary operator: brackets are its argument, and without them all that binds tighter (D41, T87)', () => {
    assert.equal(grouped('say length "abc";'), 'length["abc"]');
    assert.equal(grouped('say length("abc") . "de";'), '(length["abc"] . "de")');
    assert.equal(grouped('say length ("abc") . "de";'), '(length["abc"] . "de")');
    assert.equal(grouped('say length "abc" . "de";'), 'length[("abc" . "de")]');
    assert.equal(grouped('say length "abc" + 1 * 2;'), 'length[("abc" + (1 * 2))]');
    assert.equal(grouped('say 1 + length "ab";'), '(1 + length["ab"])');
    assert.equal(grouped('say 2 * length "ab" x 3;'), '(2 * length[("ab" x 3)])');
    assert.equal(grouped('say - length "ab" . "c";'), '(-length[("ab" . "c")])');
    assert.equal(grouped('say length -5;'), 'length[(-5)]');
    assert.equal(grouped('say uc lc "A" . "b";'), 'uc[lc[("A" . "b")]]');
    assert.equal(grouped('say ord(chr 65) + 1;'), '(ord[chr[65]] + 1)');
    assert.equal(grouped('say(length "abc");'), 'length["abc"]*');
    assert.equal(grouped('say (length "abc");'), 'length["abc"]*');
    refused('say length;', 'length needs an argument', 1, 5);
    refused('say length();', 'length needs an argument', 1, 5);
    refused('say (uc);', 'uc needs an argument', 1, 6);
    refused('say length("a", "b");', "expected ')', found ','", 1, 15);
    refused('say length * 2;', "expected a value, found '*'", 1, 12);
});

test('substr and index take their arguments in brackets (D41)', () => {
    assert.equal(grouped('say substr("abc", 1);'), 'substr["abc", 1]');
    assert.equal(grouped('say substr ("abc", 1, 1 + 1) . "d";'), '(substr["abc", 1, (1 + 1)] . "d")');
    assert.equal(grouped('say index("abc", "c", length "a");'), 'index["abc", "c", length["a"]]');
    refused('say substr "abc", 1;', 'substr needs brackets round its arguments: substr(...)', 1, 5);
    refused('say index;', 'index needs brackets round its arguments: index(...)', 1, 5);
    refused('say substr("abc");', 'substr takes 2 to 3 arguments, and here are 1', 1, 5);
    refused('say substr();', 'substr takes 2 to 3 arguments, and here are 0', 1, 5);
    refused('say index("a", "b", 0, 1);', 'index takes 2 to 3 arguments, and here are 4', 1, 5);
    refused('say substr("abc", 1,);', "expected a value, found ')'", 1, 21);
    refused('say substr("abc" 1);', "expected ')', found 1", 1, 18);
});

test('say and print take one argument, and are statements', () => {
    assert.equal(grouped('print "a" . "b";'), '("a" . "b")');
    assert.equal(grouped('print("a");'), '"a"*');
    refused('say "a", "b";', "',' after say's argument: a list is not in the language yet", 1, 8);
    refused('print("a", "b");', "expected ')', found ','", 1, 10);
    refused('say 1 + say 2;', 'say is a statement, and has no value', 1, 9);
    refused('say print "a";', 'print is a statement, and has no value', 1, 5);
    refused('print ("a") . "b";', "'.' after print (...): perl takes the brackets for all of print's arguments; bracket the whole expression", 1, 13);
    refused('print ("a") x 2;', "'x' after print (...): perl takes the brackets for all of print's arguments; bracket the whole expression", 1, 13);
    refused('print ("a"\n);', "print (...) after one blank: perl warns unless the brackets close on this line, one in a string counting too, with ';' after them: write print(...)", 1, 7);
});

test('use takes a version, or a pragma and its arguments', () => {
    assert.deepEqual(parse(lex("use utf8;\nuse open ':std', \":x\";")).body, [
        { kind: 'pragma', name: 'utf8', args: [], pos: { line: 1, col: 1 } },
        { kind: 'pragma', name: 'open', pos: { line: 2, col: 1 }, args: [
            { kind: 'str', text: "':std'", value: ':std', pos: { line: 2, col: 10 } },
            { kind: 'str', text: '":x"', value: ':x', pos: { line: 2, col: 18 } },
        ] },
    ]);
    refused('use strict;', "'use strict' is not in the language", 1, 5);
    refused('use warnings;', "'use warnings' is not in the language", 1, 5);
    refused('use 5;', "after 'use', expected a version or a pragma, found 5", 1, 5);
    refused('use "utf8";', "after 'use', expected a version or a pragma, found \"utf8\"", 1, 5);
    refused('use', "after 'use', expected a version or a pragma, found the end of the file", 1, 4);
    refused('use utf8', "expected a value, found the end of the file", 1, 9);
    // The lexer is first: a colon outside a string.
    refused('use open qw(:std);', "':' is not in the language yet", 1, 13);
    refused('use open qw(std);', "expected a value, found 'qw'", 1, 10);
    refused('use v5.42 say 1;', "expected ';', found 'say'", 1, 11);
});

test('where an operand is wanted', () => {
    const wanted = (found: string) => `expected a value, found ${found}`;
    refused('say;', wanted("';'"), 1, 4);
    refused('say 1 + ;', wanted("';'"), 1, 9);
    refused('say 1 +', wanted('the end of the file'), 1, 8);
    refused('say -;', wanted("';'"), 1, 6);
    refused('say ();', wanted("')'"), 1, 6);
    refused('say (+);', wanted("')'"), 1, 7);
    refused('say use 1;', wanted("'use'"), 1, 5);
    refused('say x 3;', wanted("'x'"), 1, 5);
    refused('say v5.42;', wanted('v5.42'), 1, 5);
    // perl has a glob `*3` and a hash `%2` here.
    refused('say 2 * *3;', wanted("'*'"), 1, 9);
    refused('say * 2;', wanted("'*'"), 1, 5);
    refused('say % 2;', wanted("'%'"), 1, 5);
    refused('say 1 % % 2;', wanted("'%'"), 1, 9);
});

test('where an operator or an end is wanted', () => {
    refused('say 1 2;', "expected ';', found 2", 1, 7);
    refused('say 1.5 5;', "expected ';', found 5", 1, 9);
    refused('say "a" "b";', "expected ';', found \"b\"", 1, 9);
    refused('say "a" "a string of more than twenty";', "expected ';', found a string", 1, 9);
    refused('say 1 (2);', "expected ';', found '('", 1, 7);
    refused('say(1 + 2;', "expected ')', found ';'", 1, 10);
    refused('say 1 + 2);', "expected ';', found ')'", 1, 10);
    refused('say (1) (2);', "expected ';', found '('", 1, 9);
    refused('say 1 + (2 3);', "expected ')', found 3", 1, 12);
    // One of perl's operators that is a word.
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
    const message = "say (...) after one blank: perl warns unless the brackets close on this line, one in a string counting too, with ';' after them: write say(...)";
    refused('say (1 +\n2);', message, 1, 5);
    refused('say (1 + 2)\n;', message, 1, 5);
    refused('say (1 + 2) # then\n;', message, 1, 5);
    refused('say (\n1);', message, 1, 5);
    // perl goes by the text: a bracket in a string counts (T100).
    refused('say ("(");', message, 1, 5);
    refused('say (")" . "a");', message, 1, 5);
    refused('say (1) # and then\n;', message, 1, 5);
    assert.equal(grouped('say (1); # and ('), '1*');
    assert.equal(grouped('say\t("(");'), '"("*');
    assert.equal(grouped('say  ("(");'), '"("*');
    assert.equal(grouped('say("(");'), '"("*');
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
