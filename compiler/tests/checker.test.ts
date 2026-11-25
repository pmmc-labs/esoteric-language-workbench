import { test } from 'node:test';
import assert from 'node:assert/strict';
import { lex } from '../src/lexer.ts';
import { parse } from '../src/parser.ts';
import { check } from '../src/checker.ts';
import { CompileError } from '../src/errors.ts';

const accepted = (src: string) => check(parse(lex(src)));
const refused = (src: string, message: string, line: number, col: number) =>
    assert.throws(() => accepted(src), (e: unknown) => {
        assert.ok(e instanceof CompileError, String(e));
        assert.deepEqual([e.message, e.line, e.col], [message, line, col]);
        return true;
    });

test('programs', () => {
    accepted('use v5.42;');
    accepted('# a comment\nuse v5.42;\nsay 0;\nsay 9223372036854775807;');
    accepted('use\nv5.42\n;say\n1\n;');
});

test("a program begins 'use v5.42;'", () => {
    const message = "a program begins 'use v5.42;'";
    refused('', message, 1, 1);
    refused('# nothing\n', message, 2, 1);
    refused('\n say 42;', message, 2, 2);
    refused('say 42;\nuse v5.42;', message, 1, 1);
    refused('use v5.36;\nsay 42;', message, 1, 1);
    refused('use v5.42.0;', message, 1, 1);
    refused('use v5;', message, 1, 1);
});

test('the version is said once', () => {
    refused('use v5.42;\nuse v5.42;', "'use v5.42;' here: the version is the first statement, and is said once", 2, 1);
    refused('use v5.42; say 1; use v5.36;', "'use v5.36;' here: the version is the first statement, and is said once", 1, 19);
});

test('the pragmas: a closed list, each written one way, at the top, once (D16, D39)', () => {
    accepted("use v5.42;\nuse utf8;\nuse open ':std', ':encoding(UTF-8)';\nsay 1;");
    accepted('use v5.42;\nuse open ":std", ":encoding(UTF-8)";\nuse utf8;');
    accepted('use v5.42; use open ":s\\x74d", \':encoding(UTF-8)\';');
    const open = "'use open' is written: use open ':std', ':encoding(UTF-8)';";
    refused("use v5.42;\nuse open;", open, 2, 1);
    refused("use v5.42;\nuse open ':std';", open, 2, 1);
    refused("use v5.42;\nuse open ':std', ':utf8';", open, 2, 1);
    refused("use v5.42;\nuse open ':encoding(UTF-8)', ':std';", open, 2, 1);
    refused("use v5.42;\nuse open ':std', ':encoding(UTF-8)', ':std';", open, 2, 1);
    refused("use v5.42;\nuse open ':std', ':encoding(utf-8)';", open, 2, 1);
    refused("use v5.42;\nuse open (':std'), ':encoding(UTF-8)';", open, 2, 1);
    refused("use v5.42;\nuse open ':std' . '', ':encoding(UTF-8)';", open, 2, 1);
    refused("use v5.42;\nuse utf8 'x';", "'use utf8' is written: use utf8;", 2, 1);
    refused('use v5.42;\nuse utf8;\nuse utf8;', "'use utf8' is said once", 3, 1);
    refused("use v5.42;\nsay 1;\nuse utf8;", "'use utf8' goes at the top, after 'use v5.42;' and before anything else", 3, 1);
    refused("use utf8;\nuse v5.42;", "a program begins 'use v5.42;'", 1, 1);
});

test("x with its left operand in brackets, as say's argument, repeats a list to perl (T101)", () => {
    const message = (name: string) => `(...) x as ${name}'s argument repeats a list, to perl: take the brackets off the left operand`;
    refused('use v5.42;\nsay(("a") x 3);', message('say'), 2, 11);
    refused('use v5.42;\nsay ("a") x 3;', "'x' after say (...): perl takes the brackets for all of say's arguments; bracket the whole expression", 2, 11);
    refused('use v5.42;\nprint +("a") x 3;', message('print'), 2, 14);
    refused('use v5.42;\nsay((("a" . "b")) x 2);', message('say'), 2, 19);
    refused('use v5.42;\nsay +(+("a") x 2);', message('say'), 2, 14);
    // In a string's place it is a string that is repeated.
    accepted('use v5.42;\nsay "a" x 3;\nsay(("a") x 3 . "b");\nsay length(("a") x 3);\nsay -("2") x 3;\nsay "" . ("a") x 3;\nsay(("a" x 2) . "");');
    accepted('use v5.42;\nsay(("a" x 3));\nsay "a" x (3);');
});

test('a string, a builtin and its arguments are checked through', () => {
    accepted('use v5.42;\nsay length("abc") . substr("abc", 1, 2) x 2;');
    refused('use v5.42;\nsay substr("abc", 01);', '01 starts with a zero: perl reads that as octal, which the language writes 0o17', 2, 19);
    refused('use v5.42;\nsay length 0xFFFFFFFFF;', '0xFFFFFFFFF is past 32 bits, where perl warns that a literal is not portable', 2, 12);
    refused('use v5.42;\nprint "a" . 9223372036854775808;', '9223372036854775808 is past the largest integer, 9223372036854775807', 2, 13);
});

test('an integer has no leading zero (T24)', () => {
    accepted('use v5.42; say 0;');
    const zero = (text: string) => `${text} starts with a zero: perl reads that as octal, which the language writes 0o17`;
    refused('use v5.42;\nsay 010;', zero('010'), 2, 5);
    refused('use v5.42;\nsay 08;', zero('08'), 2, 5);
    refused('use v5.42; say 00;', zero('00'), 1, 16);
    refused('use v5.42; say 0_17;', zero('0_17'), 1, 16);
    refused('use v5.42; say 00.5;', zero('00.5'), 1, 16);
    refused('use v5.42; say 01e3;', zero('01e3'), 1, 16);
    accepted('use v5.42; say 0.5; say 0e0; say 0x0; say 1e007; say 0.007;');
});

test('every literal in an expression is checked', () => {
    accepted('use v5.42; say -(1 + 2) * +3 % 4;');
    refused('use v5.42;\nsay 1 + 010;', '010 starts with a zero: perl reads that as octal, which the language writes 0o17', 2, 9);
    refused('use v5.42;\nsay -(2 * (3 - 07));', '07 starts with a zero: perl reads that as octal, which the language writes 0o17', 2, 16);
    refused('use v5.42;\nsay 2 ** (1 / 1e999);', '1e999 is past the largest float', 2, 15);
    // The smallest Int has no literal: its digits are past the largest.
    refused('use v5.42;\nsay -9223372036854775808;', '9223372036854775808 is past the largest integer, 9223372036854775807', 2, 6);
    accepted('use v5.42; say -9223372036854775807 - 1;');
});

test('a hex, binary or octal literal is at most 32 bits (D38)', () => {
    const past = (text: string) => `${text} is past 32 bits, where perl warns that a literal is not portable`;
    accepted('use v5.42; say 0xFFFFFFFF; say 0b11111111111111111111111111111111; say 0o37777777777;');
    refused('use v5.42; say 0x100000000;', past('0x100000000'), 1, 16);
    refused('use v5.42; say 0b100000000000000000000000000000000;', past('0b100000000000000000000000000000000'), 1, 16);
    refused('use v5.42; say 0o40000000000;', past('0o40000000000'), 1, 16);
    refused('use v5.42; say 0xFFFF_FFFF_F;', past('0xFFFF_FFFF_F'), 1, 16);
});

test('a decimal literal is at most 250 characters, underscores aside (T91)', () => {
    const long = 'a number of more than 250 characters: perl refuses it as too long';
    accepted(`use v5.42; say 1.${'0'.repeat(248)};`);
    refused(`use v5.42; say 1.${'0'.repeat(249)};`, long, 1, 16);
    accepted(`use v5.42; say 0.${'1_'.repeat(247)}1;`);
    refused(`use v5.42; say 0.${'1_'.repeat(249)}1;`, long, 1, 16);
    refused(`use v5.42; say 1e${'0'.repeat(249)}1;`, long, 1, 16);
    accepted(`use v5.42; say 0x${'0'.repeat(300)}1F;`);
});

test('a float is finite (D37)', () => {
    accepted('use v5.42; say 1.7976931348623157e308; say 1e-400; say 5e-324;');
    refused('use v5.42; say 1e400;', '1e400 is past the largest float', 1, 16);
    refused('use v5.42; say 1.8e308;', '1.8e308 is past the largest float', 1, 16);
});

test('an integer is at most 2^63 - 1 (D23)', () => {
    refused('use v5.42;\nsay 9223372036854775808;', '9223372036854775808 is past the largest integer, 9223372036854775807', 2, 5);
    refused('use v5.42; say 99999999999999999999999999;', '99999999999999999999999999 is past the largest integer, 9223372036854775807', 1, 16);
});

test("the list that say's argument is reaches the right of || and both branches of ? : (T104)", () => {
    const message = "(...) x as say's argument repeats a list, to perl: take the brackets off the left operand";
    refused('use v5.42;\nsay(0 || ("a") x 3);', message, 2, 16);
    refused('use v5.42;\nsay(1 && ("a") x 3);', message, 2, 16);
    refused('use v5.42;\nsay(undef // ("a") x 3);', message, 2, 20);
    refused('use v5.42;\nsay(0 or 1 and ("a") x 3);', message, 2, 22);
    refused('use v5.42;\nsay 1 ? ("a") x 3 : "b";', message, 2, 15);
    refused('use v5.42;\nsay 0 ? "b" : 1 ? 2 : (("a")) x 3;', message, 2, 31);
    refused('use v5.42;\nsay 0 || +("a") x 3;', message, 2, 17);
    accepted('use v5.42;\nsay(("a") x 3 || 0);\nsay((("a") x 3) ? 1 : 2);\nsay(1 xor ("a") x 3);\nsay(!("a") x 3);\nsay(("a") x 3 eq "aaa");\nsay(0 || "" . ("a") x 3);');
});
