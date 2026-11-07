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

// Step 2: scopes (D12).
const fails = (src: string, message: string, line: number, col: number) =>
  assert.throws(
    () => run(src),
    (e: any) => e.message === message && e.pos.line === line && e.pos.col === col,
    `${JSON.stringify(src)}: expected ${message} at ${line}:${col}`,
  );

test('a variable is visible after its let, in nested blocks, until its block ends', () => {
  run('let x = 1\nprint(x)\nif true { print(x); let y = x\n x = y }\nwhile false { x += 1 }');
  fails('print(x)\nlet x = 1', 'unknown variable x', 1, 7);
  fails('if true { let a = 1 }\nprint(a)', 'unknown variable a', 2, 7);
  fails('for i in 0..3 { }\nprint(i)', 'unknown variable i', 2, 7);
  fails('while true { let w = 1 }\nw = 2', 'unknown variable w', 2, 1);
});

test('let x = x + 1 is an unknown variable; the new name is not yet in scope', () => {
  fails('let x = x + 1', 'unknown variable x', 1, 9);
  fails('let x = 1\nlet y = y', 'unknown variable y', 2, 9);
});

test('no shadowing, but sibling blocks may reuse a name', () => {
  run('if true { let t = 1 }\nif true { let t = 2 }\nfor i in 0..2 { let j = i }\nfor i in 0..2 { let j = i }');
  run('if true { let t = 1 }\nlet t = 2');
  fails('let x = 1\nlet x = 2', 'x is already declared', 2, 5);
  fails('let x = 1\nif true {\n  let x = 2\n}', 'x is already declared', 3, 7);
  fails('let i = 0\nfor i in 0..1 { }', 'i is already declared', 2, 5);
  fails('for i in 0..1 { let i = 2 }', 'i is already declared', 1, 21);
  fails('for i in 0..1 { for i in 0..1 { } }', 'i is already declared', 1, 21);
});

test('the range and the iterated expression cannot see the loop variable', () => {
  fails('for i in 0..i { }', 'unknown variable i', 1, 13);
  fails('for i in i { }', 'unknown variable i', 1, 10);
});

test('assignment checks the target, then the value', () => {
  fails('y = z', 'unknown variable y', 1, 1);
  fails('let a = 1\na += z', 'unknown variable z', 2, 6);
  fails('let a = 1\n  q -= a', 'unknown variable q', 2, 3);
});

test('break and continue need a loop', () => {
  fails('break', 'break outside a loop', 1, 1);
  fails('print(1)\n  continue', 'continue outside a loop', 2, 3);
  fails('if true { break }', 'break outside a loop', 1, 11);
  fails('while true { }\nbreak', 'break outside a loop', 2, 1);
  run('while true { if true { break } else { continue } }');
  run('for i in 0..3 { while true { break }\n continue }');
});

test('a builtin used as a value is not a value; a statement of a name is not a call', () => {
  fails('let f = print', 'functions are not values', 1, 9);
  fails('print(print)', 'functions are not values', 1, 7);
  fails('let x = 1\nx', 'expression statement must be a call', 2, 1);
});

test('variable uses are annotated with their C name; the input is unchanged', () => {
  const p = parse(lex('let abc = 1\nprint(abc)'));
  const before = JSON.stringify(p, (_k, v) => (typeof v === 'bigint' ? String(v) : v));
  const r = resolve(p) as any;
  assert.equal(r.body[1].expr.args[0].cname, 'v_abc');
  assert.equal(JSON.stringify(p, (_k, v) => (typeof v === 'bigint' ? String(v) : v)), before);
});

test('the first error in source order is the one reported', () => {
  fails('print(a)\nprint(b)\nbreak', 'unknown variable a', 1, 7);
  fails('break\nprint(b)', 'break outside a loop', 1, 1);
  fails('let x = 1\nlet x = y', 'x is already declared', 2, 5);
});
