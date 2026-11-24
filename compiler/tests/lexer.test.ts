import { test } from 'node:test';
import assert from 'node:assert/strict';
import { lex } from '../src/lexer.ts';
import { CompileError } from '../src/errors.ts';

const refused = (src: string, message: string, line: number, col: number) =>
    assert.throws(() => lex(src), (e: unknown) => {
        assert.ok(e instanceof CompileError, String(e));
        assert.deepEqual([e.message, e.line, e.col], [message, line, col]);
        return true;
    });

test('tokens, each with its line and column', () => {
    const tokens = lex('# first\nuse v5.42;\n\tsay 42;  # after\n say\n9223372036854775807 ;');
    assert.deepEqual(tokens.map(t => [t.kind, t.text, t.pos.line, t.pos.col]), [
        ['word', 'use', 2, 1], ['version', 'v5.42', 2, 5], [';', ';', 2, 10],
        ['word', 'say', 3, 2], ['int', '42', 3, 6], [';', ';', 3, 8],
        ['word', 'say', 4, 2], ['int', '9223372036854775807', 5, 1], [';', ';', 5, 21],
        ['eof', '', 5, 22],
    ]);
});

test('an empty file is its end, and a comment needs no newline after it', () => {
    assert.deepEqual(lex(''), [{ kind: 'eof', text: '', pos: { line: 1, col: 1 } }]);
    assert.deepEqual(lex('\n  # only this').at(-1), { kind: 'eof', text: '', pos: { line: 2, col: 14 } });
});

test('a version literal is v, digits, and groups of .digits', () => {
    const kinds = (src: string) => lex(src).map(t => `${t.kind} ${t.text}`.trim());
    assert.deepEqual(kinds('v5.42'), ['version v5.42', 'eof']);
    assert.deepEqual(kinds('v5.42.0'), ['version v5.42.0', 'eof']);
    assert.deepEqual(kinds('v5'), ['version v5', 'eof']);
    assert.deepEqual(kinds('v v5x value'), ['word v', 'word v5x', 'word value', 'eof']);
});

test('a version ends at a blank or a semicolon, as perl has it (T75)', () => {
    const message = (c: string) => `v5.42 runs into '${c}': perl reads a version only before a blank or ';'`;
    refused('use v5.42#c\n;', message('#'), 1, 5);
    refused('use v5.42# c\n;', message('#'), 1, 5);
    refused('v5.42.;', message('.'), 1, 1);
    refused('v5.42x;', message('x'), 1, 1);
    assert.equal(lex('use v5.42 #c\n;').length, 4);
    assert.equal(lex('use v5.42\t;').length, 4);
    assert.equal(lex('use v5.42\n;').length, 4);
    assert.equal(lex('use v5.42').length, 3);
    refused('use v5.42\r\n;', 'a control character (U+000D) is not in the language', 1, 10);
});

test('a number that runs into a word is neither', () => {
    refused('say 1_000;', '1_000: the only numbers so far are decimal integers', 1, 5);
    refused('say 0x10;', '0x10: the only numbers so far are decimal integers', 1, 5);
    refused('say 1e3;', '1e3: the only numbers so far are decimal integers', 1, 5);
    refused('say 42x3;', '42x3: the only numbers so far are decimal integers', 1, 5);
});

test('brackets and operators', () => {
    const tokens = lex('say(1+-2 %3)\n* 4;');
    assert.deepEqual(tokens.map(t => [t.kind, t.text, t.pos.line, t.pos.col]), [
        ['word', 'say', 1, 1], ['(', '(', 1, 4], ['int', '1', 1, 5], ['op', '+', 1, 6], ['op', '-', 1, 7],
        ['int', '2', 1, 8], ['op', '%', 1, 10], ['int', '3', 1, 11], [')', ')', 1, 12],
        ['op', '*', 2, 1], ['int', '4', 2, 3], [';', ';', 2, 4], ['eof', '', 2, 5],
    ]);
});

test("the longest of perl's operators is the token, in the language or not (T27)", () => {
    refused('say --5;', "'--' is not in the language yet", 1, 5);
    refused('say 1--2;', "'--' is not in the language yet", 1, 6);
    refused('say ++5;', "'++' is not in the language yet", 1, 5);
    refused('say 2 ** 3;', "'**' is not in the language yet", 1, 7);
    refused('say 2 **= 3;', "'**=' is not in the language yet", 1, 7);
    refused('say 1 <=> 2;', "'<=>' is not in the language yet", 1, 7);
    refused('say 1 -> 2;', "'->' is not in the language yet", 1, 7);
    refused('say 7 %= 2;', "'%=' is not in the language yet", 1, 7);
    refused('say 1.5;', "'.' is not in the language yet", 1, 6);
    refused('say 1 / 2;', "'/' is not in the language yet", 1, 7);
    refused('say 1, 2;', "',' is not in the language yet", 1, 6);
    // With a blank between them they are two, as they are to perl.
    assert.deepEqual(lex('- - + +').map(t => t.text), ['-', '-', '+', '+', '']);
});

test('a character the language has no use for yet', () => {
    refused('say "x";', "'\"' is not in the language yet", 1, 5);
    refused('say $x;', "'$' is not in the language yet", 1, 5);
    refused('say {1};', "'{' is not in the language yet", 1, 5);
});

test('a character past ASCII, wherever it stands', () => {
    refused('say 42; # café', 'a character past ASCII (U+00E9) is not in the language yet', 1, 14);
    refused('\nsay é;', 'a character past ASCII (U+00E9) is not in the language yet', 2, 5);
    refused('# \u{1F600}', 'a character past ASCII (U+1F600) is not in the language yet', 1, 3);
    // What the driver makes of bytes that aren't UTF-8, and a byte order mark.
    refused('say �;', 'a character past ASCII (U+FFFD) is not in the language yet', 1, 5);
    refused('﻿use v5.42;', 'a character past ASCII (U+FEFF) is not in the language yet', 1, 1);
});

test('a control character, wherever it stands', () => {
    refused('use v5.42;\r\nsay 42;', 'a control character (U+000D) is not in the language', 1, 11);
    refused('say 1; # \x04', 'a control character (U+0004) is not in the language', 1, 10);
    refused('say 1;\x1a', 'a control character (U+001A) is not in the language', 1, 7);
    refused('\x00', 'a control character (U+0000) is not in the language', 1, 1);
    refused('say\x0c1;', 'a control character (U+000C) is not in the language', 1, 4);
    refused('# \x7f', 'a control character (U+007F) is not in the language', 1, 3);
});

test("a line that starts '#!', the first or any other (T72)", () => {
    const message = "a line that starts '#!' is not in the language: perl can take switches from it";
    refused('#!/usr/bin/perl -n\nuse v5.42;', message, 1, 1);
    refused('#!', message, 1, 1);
    refused(' \t#!perl', message, 1, 3);
    refused('\n#!/usr/bin/perl -n\nuse v5.42;', message, 2, 1);
    refused('use v5.42;\n# line 1\n  #!perl -n\nsay 2;', message, 3, 3);
    refused('use v5.42;\nsay\n#!perl\n1;', message, 3, 1);
    // After a token on its line, or after another `#`, it is a comment.
    assert.equal(lex('use v5.42; #!perl -n').length, 4);
    assert.equal(lex('# !perl -n\n# #!perl -n\n##!').length, 1);
});
