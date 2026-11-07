import { test } from 'node:test';
import assert from 'node:assert/strict';
import { lex } from '../src/lexer.ts';
import { parse } from '../src/parser.ts';
import { resolve } from '../src/resolve.ts';

const run = (src: string) => resolve(parse(lex(src)));

test('print resolves to a builtin', () => {
  const p = run('print(1)\nprint()');
  assert.equal(p.body.length, 2);
  for (const s of p.body) assert.equal((s as any).expr.target, 'builtin');
});

test('an unknown function is an error at the name', () => {
  assert.throws(
    () => run('print(1)\n  foo(2)'),
    (e: any) => e.message === 'unknown function foo' && e.pos.line === 2 && e.pos.col === 3,
  );
});

test('only the first error is reported', () => {
  assert.throws(() => run('bar(1)\nfoo(2)'), (e: any) => e.message === 'unknown function bar');
});

test('the input is not changed', () => {
  const parsed = parse(lex('print(1)'));
  const before = JSON.stringify(parsed, (_k, v) => (typeof v === 'bigint' ? String(v) : v));
  resolve(parsed);
  assert.equal(JSON.stringify(parsed, (_k, v) => (typeof v === 'bigint' ? String(v) : v)), before);
});

test('an expression statement must be a call, at its first token', () => {
  for (const src of ['42', 'true', '-print(1)', 'nil', '1 +\n2', 'not true']) {
    assert.throws(
      () => run(`print(1)\n  ${src}`),
      (e: any) => e.message === 'expression statement must be a call' && e.pos.line === 2 && e.pos.col === 3,
      src,
    );
  }
});

test('calls nested in operators are resolved', () => {
  assert.throws(() => run('print(1 + foo(2))'), (e: any) => e.message === 'unknown function foo' && e.pos.col === 11);
  assert.throws(() => run('print(not foo())'), (e: any) => e.message === 'unknown function foo');
  assert.throws(() => run('print(true and foo())'), (e: any) => e.message === 'unknown function foo');
  const p = run('print(1 + print(2) == nil)');
  assert.equal((p.body[0] as any).expr.args[0].left.right.target, 'builtin');
});
