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

test('and has no other use', () => {
    refused('use v5.42;\nuse v5.42;', "'use v5.42;' here: the only 'use' so far is the first statement", 2, 1);
    refused('use v5.42; say 1; use v5.36;', "'use v5.36;' here: the only 'use' so far is the first statement", 1, 19);
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

test('a float is finite (D37)', () => {
    accepted('use v5.42; say 1.7976931348623157e308; say 1e-400; say 5e-324;');
    refused('use v5.42; say 1e400;', '1e400 is past the largest float', 1, 16);
    refused('use v5.42; say 1.8e308;', '1.8e308 is past the largest float', 1, 16);
});

test('an integer is at most 2^63 - 1 (D23)', () => {
    refused('use v5.42;\nsay 9223372036854775808;', '9223372036854775808 is past the largest integer, 9223372036854775807', 2, 5);
    refused('use v5.42; say 99999999999999999999999999;', '99999999999999999999999999 is past the largest integer, 9223372036854775807', 1, 16);
});
