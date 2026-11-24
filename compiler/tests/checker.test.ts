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
    refused('use v5.42;\nsay 010;', '010 starts with a zero, which perl reads as octal: not in the language yet', 2, 5);
    refused('use v5.42;\nsay 08;', '08 starts with a zero, which perl reads as octal: not in the language yet', 2, 5);
    refused('use v5.42; say 00;', '00 starts with a zero, which perl reads as octal: not in the language yet', 1, 16);
});

test('an integer is at most 2^63 - 1 (D23)', () => {
    refused('use v5.42;\nsay 9223372036854775808;', '9223372036854775808 is past the largest integer, 9223372036854775807', 2, 5);
    refused('use v5.42; say 99999999999999999999999999;', '99999999999999999999999999 is past the largest integer, 9223372036854775807', 1, 16);
});
