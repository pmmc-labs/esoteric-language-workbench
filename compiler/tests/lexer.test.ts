import { test } from 'node:test';
import assert from 'node:assert/strict';
import { lex } from '../src/lexer.ts';
import type { Token } from '../src/lexer.ts';

// The source is the file's bytes as a latin1 string, so one char is one byte.
const show = (tokens: Token[]) =>
  tokens.map((t) => `${t.kind}:${t.kind === 'newline' ? '\\n' : t.text}@${t.pos.line}:${t.pos.col}`);
const toks = (src: string) => show(lex(src));

function lexError(src: string, message: string, line: number, col: number) {
  assert.throws(
    () => lex(src),
    (e: any) => e.message === message && e.pos.line === line && e.pos.col === col,
    `${JSON.stringify(src)}: expected ${message} at ${line}:${col}`,
  );
}

test('empty source is just end of file', () => {
  assert.deepEqual(toks(''), ['eof:@1:1']);
  assert.deepEqual(toks('  \t // only a comment'), ['eof:@1:22']);
});

test('a call', () => {
  assert.deepEqual(toks('print(42)'), [
    'name:print@1:1', 'op:(@1:6', 'int:42@1:7', 'op:)@1:9', 'eof:@1:10',
  ]);
});

test('every keyword is a keyword, near-misses are names', () => {
  const kws = 'and break continue else false fn for if in let nil not or return true while'.split(' ');
  for (const k of kws) assert.deepEqual(toks(k).slice(0, 1), [`kw:${k}@1:1`]);
  assert.deepEqual(toks('letter _if If').slice(0, 3), ['name:letter@1:1', 'name:_if@1:8', 'name:If@1:12']);
});

test('names may hold digits and underscores', () => {
  assert.deepEqual(toks('_a1 b_2 __').slice(0, 3), ['name:_a1@1:1', 'name:b_2@1:5', 'name:__@1:9']);
});

test('operators and punctuation, longest match first', () => {
  const src = '== != <= >= += -= *= /= %= ..= .. < > = + - * / % . , ; : ( ) [ ] { }';
  const want = src.split(' ');
  const got = lex(src).filter((t) => t.kind === 'op').map((t) => t.text);
  assert.deepEqual(got, want);
  assert.deepEqual(toks('a..=b').slice(0, 3), ['name:a@1:1', 'op:..=@1:2', 'name:b@1:5']);
  assert.deepEqual(toks('1..5').slice(0, 3), ['int:1@1:1', 'op:..@1:2', 'int:5@1:4']);
  assert.deepEqual(toks('a!=b').slice(0, 3), ['name:a@1:1', 'op:!=@1:2', 'name:b@1:4']);
});

test('integer values', () => {
  const v = (s: string) => (lex(s)[0] as any).value;
  assert.equal(v('0'), 0n);
  assert.equal(v('1_000_000'), 1000000n);
  assert.equal(v('9223372036854775807'), 9223372036854775807n);
  assert.equal(v('9_223_372_036_854_775_807'), 9223372036854775807n);
  assert.equal(v('0007'), 7n);
  assert.equal(lex('1_000')[0].text, '1_000');
});

test('a newline run is one newline token; leading newlines are dropped', () => {
  assert.deepEqual(toks('a\n\n\nb'), ['name:a@1:1', 'newline:\\n@1:2', 'name:b@4:1', 'eof:@4:2']);
  assert.deepEqual(toks('\n\na'), ['name:a@3:1', 'eof:@3:2']);
  assert.deepEqual(toks('a // c\n// d\n\nb'), ['name:a@1:1', 'newline:\\n@1:7', 'name:b@4:1', 'eof:@4:2']);
  assert.deepEqual(toks('a\n'), ['name:a@1:1', 'newline:\\n@1:2', 'eof:@2:1']);
});

test('carriage returns are whitespace', () => {
  assert.deepEqual(toks('a\r\nb'), ['name:a@1:1', 'newline:\\n@1:3', 'name:b@2:1', 'eof:@2:2']);
});

test('newlines are dropped inside ( ) and [ ] but kept inside { }', () => {
  assert.deepEqual(toks('f(\n1,\n2\n)\nx'), [
    'name:f@1:1', 'op:(@1:2', 'int:1@2:1', 'op:,@2:2', 'int:2@3:1', 'op:)@4:1',
    'newline:\\n@4:2', 'name:x@5:1', 'eof:@5:2',
  ]);
  assert.deepEqual(toks('[1,\n2]\n').map((s) => s.split('@')[0]), [
    'op:[', 'int:1', 'op:,', 'int:2', 'op:]', 'newline:\\n', 'eof:',
  ]);
  assert.deepEqual(toks('{\n}').map((s) => s.split('@')[0]), ['op:{', 'newline:\\n', 'op:}', 'eof:']);
  assert.equal(toks('x = {\na: 1\n}').filter((s) => s.startsWith('newline')).length, 2);
  assert.equal(toks('f([\n1\n],\n{\na: 1\n})').filter((s) => s.startsWith('newline')).length, 0);
});

test('a stray closer does not make later newlines vanish', () => {
  assert.deepEqual(toks(')\na').map((s) => s.split('@')[0]), ['op:)', 'newline:\\n', 'name:a', 'eof:']);
});

test('semicolons are tokens', () => {
  assert.deepEqual(toks('a;b').slice(0, 3), ['name:a@1:1', 'op:;@1:2', 'name:b@1:3']);
});

test('columns count bytes, tabs count one', () => {
  assert.deepEqual(toks('\tx').slice(0, 1), ['name:x@1:2']);
  assert.deepEqual(toks('"\xc3\xa9" x').slice(1, 2), ['name:x@1:6']);
  assert.deepEqual(toks('x // \xc3\xa9\ny').slice(1, 3), ['newline:\\n@1:8', 'name:y@2:1']);
});

const parts = (src: string) => (lex(src)[0] as any).parts;

test('string tokens', () => {
  assert.equal(lex('"ab"')[0].kind, 'string');
  assert.equal(lex('"ab"')[0].text, '"ab"');
  assert.deepEqual(parts('"ab"'), [{ kind: 'text', value: 'ab' }]);
  assert.deepEqual(parts('""'), []);
  assert.deepEqual(parts('"\xc3\xa9"'), [{ kind: 'text', value: '\xc3\xa9' }]);
  assert.deepEqual(parts('"a\\n\\t\\r\\\\\\"\\{\\}b"'), [{ kind: 'text', value: 'a\n\t\r\\"{}b' }]);
  assert.deepEqual(parts('"a}b"'), [{ kind: 'text', value: 'a}b' }]);
  assert.deepEqual(parts('"// not a comment"'), [{ kind: 'text', value: '// not a comment' }]);
});

test('interpolation', () => {
  const p = parts('"a{x + 1}b"');
  assert.equal(p.length, 3);
  assert.deepEqual(p[0], { kind: 'text', value: 'a' });
  assert.equal(p[1].kind, 'interp');
  assert.deepEqual(p[1].pos, { line: 1, col: 3 });
  assert.deepEqual(show(p[1].tokens), ['name:x@1:4', 'op:+@1:6', 'int:1@1:8']);
  assert.deepEqual(p[2], { kind: 'text', value: 'b' });
});

test('adjacent interpolations, and one alone', () => {
  const p = parts('"{a}{b}"');
  assert.deepEqual(p.map((x: any) => x.kind), ['interp', 'interp']);
  assert.deepEqual(show(p[1].tokens), ['name:b@1:6']);
});

test('interpolation holds strings, nesting, and braces', () => {
  const p = parts('"{f("x{y}")}"');
  assert.equal(p.length, 1);
  const inner = p[0].tokens;
  assert.deepEqual(inner.map((t: Token) => t.kind), ['name', 'op', 'string', 'op']);
  assert.deepEqual(inner[2].parts[1].pos, { line: 1, col: 7 });
  assert.deepEqual(show(inner[2].parts[1].tokens), ['name:y@1:8']);
  const q = parts('"{ {a: 1}[0] }"');
  assert.deepEqual(show(q[0].tokens).map((s: string) => s.split('@')[0]),
    ['op:{', 'name:a', 'op::', 'int:1', 'op:}', 'op:[', 'int:0', 'op:]']);
});

test('tokens after a string carry on at the right column', () => {
  assert.deepEqual(toks('"a{1}b" x').slice(1, 2), ['name:x@1:9']);
});

test('unexpected characters', () => {
  for (const c of '!&|$@#`~^?\'\\') lexError(`x ${c}`, `unexpected character '${c}'`, 1, 3);
  lexError('a\n  #', "unexpected character '#'", 2, 3);
});

test('unexpected bytes', () => {
  lexError('x \xc3\xa9', 'unexpected byte 0xC3', 1, 3);
  lexError('\x01', 'unexpected byte 0x01', 1, 1);
  lexError('\x7f', 'unexpected byte 0x7F', 1, 1);
  lexError('\xff', 'unexpected byte 0xFF', 1, 1);
});

test('malformed numbers point at the first byte', () => {
  lexError('12ab', 'malformed number', 1, 1);
  lexError('x = 1_', 'malformed number', 1, 5);
  lexError('1__0', 'malformed number', 1, 1);
  lexError('1a', 'malformed number', 1, 1);
  lexError('12_a', 'malformed number', 1, 1);
});

test('integer literal range', () => {
  assert.doesNotThrow(() => lex('9223372036854775807'));
  lexError('9223372036854775808', 'integer literal too large', 1, 1);
  lexError('x 9_223_372_036_854_775_808', 'integer literal too large', 1, 3);
  lexError('99999999999999999999999', 'integer literal too large', 1, 1);
});

test('string errors', () => {
  lexError('x "a\\qb"', "unknown escape '\\q'", 1, 5);
  lexError('"abc', 'unterminated string', 1, 1);
  lexError('x\n  "abc\ny"', 'unterminated string', 2, 3);
  lexError('"abc\\', 'unterminated string', 1, 1);
  lexError('"{x + "b}"', 'unterminated interpolation', 1, 2);
  lexError('"a{}"', 'empty interpolation', 1, 3);
  lexError('"a{  }"', 'empty interpolation', 1, 3);
  lexError('"a{1 + 2"', 'unterminated interpolation', 1, 3);
  lexError('"a{1 + 2\nx"', 'unterminated interpolation', 1, 3);
  lexError('"{#}"', "unexpected character '#'", 1, 3);
  lexError('"{12ab}"', 'malformed number', 1, 3);
});
