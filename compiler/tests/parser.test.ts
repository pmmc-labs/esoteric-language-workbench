import { test } from 'node:test';
import assert from 'node:assert/strict';
import { lex } from '../src/lexer.ts';
import { parse } from '../src/parser.ts';
import { CompileError } from '../src/errors.ts';

const refused = (src: string, message: string, line: number, col: number) =>
    assert.throws(() => parse(lex(src)), (e: unknown) => {
        assert.ok(e instanceof CompileError, String(e));
        assert.deepEqual([e.message, e.line, e.col], [message, line, col]);
        return true;
    });

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

test('what a statement may start with', () => {
    refused('use v5.42;\n;', "expected a statement, found ';'", 2, 1);
    refused('42;', 'expected a statement, found 42', 1, 1);
    refused('v5.42;', 'expected a statement, found v5.42', 1, 1);
    refused('use v5.42;\nprint 42;', "'print' is not in the language", 2, 1);
    refused('say42;', "'say42' is not in the language", 1, 1);
});

test('use takes a version', () => {
    refused('use strict;', "after 'use', expected a version, found 'strict'", 1, 5);
    refused('use 5;', "after 'use', expected a version, found 5", 1, 5);
    refused('use', "after 'use', expected a version, found the end of the file", 1, 4);
    refused('use v5.42 say 1;', "expected ';', found 'say'", 1, 11);
});

test('say takes one integer', () => {
    refused('say;', "after 'say', expected an integer, found ';'", 1, 4);
    refused('say say 1;', "after 'say', expected an integer, found 'say'", 1, 5);
    refused('say v5.42;', "after 'say', expected an integer, found v5.42", 1, 5);
    refused('say 1 2;', "expected ';', found 2", 1, 7);
});

test('every statement ends with its semicolon, and only one', () => {
    refused('use v5.42;\nsay 1', "expected ';', found the end of the file", 2, 6);
    refused('say 1\nsay 2;', "expected ';', found 'say'", 2, 1);
    refused('say 1;;', "expected a statement, found ';'", 1, 7);
});
