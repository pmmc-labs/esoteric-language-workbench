import { test } from 'node:test';
import assert from 'node:assert/strict';
import { cString, generate } from '../src/codegen.ts';
import { lex } from '../src/lexer.ts';
import { parse } from '../src/parser.ts';
import { resolve } from '../src/resolver.ts';

// What the generated C does is the golden tests' to say, by running it.
// This is the one piece they can't reach: no test's path has a quote in it.
test('a C string literal of any path', () => {
    assert.equal(cString('t/000-say.pl'), '"t/000-say.pl"');
    assert.equal(cString('a "b"\\c.pl'), '"a \\042b\\042\\134c.pl"');
    assert.equal(cString('what??/.pl'), '"what\\077\\077/.pl"');
    assert.equal(cString('café\n1.pl'), '"caf\\303\\251\\0121.pl"');
});

// A string literal is a constant with its bytes and its characters
// counted, which no golden test can see to be wrong until something reads
// the wrong one.
test('a string literal is a constant: its bytes, its characters, its UTF-8', () => {
    const tree = parse(lex('use utf8;\nsay "caf\u00e9 \u{1F600}\\0" . \'\';'));
    const c = generate(tree, resolve(tree), 'a.pl');
    assert.ok(c.includes('static const rt_str s1 = { 11, 7, "caf\\303\\251 \\360\\237\\230\\200\\000" };'), c);
    assert.ok(c.includes('static const rt_str s2 = { 0, 0, "" };'), c);
    assert.ok(c.includes('rt_concat(cx, rt_string(&s1), rt_string(&s2))'), c);
});
