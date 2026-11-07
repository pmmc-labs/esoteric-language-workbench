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

// Step 3: functions (D13).
test('calls to user functions are resolved, before or after the definition', () => {
  const p = run('print(f(1))\nfn f(a) { return g(a) }\nfn g(b) { return b }');
  assert.equal((p.body[0] as any).expr.args[0].target, 'fn');
  assert.equal((p.body[1] as any).body[0].value.target, 'fn');
  assert.equal((p.body[1] as any).params[0].cname, 'v_a');
});

test('arity: the exact number of arguments, at the name', () => {
  fails('fn f(a, b) { }\nf(1)', 'f takes 2 arguments, got 1', 2, 1);
  fails('fn f(a, b) { }\n  print(f(1, 2, 3))', 'f takes 2 arguments, got 3', 2, 9);
  fails('fn f(a) { }\nf()', 'f takes 1 argument, got 0', 2, 1);
  fails('fn f(a) { }\nf(1, 2)', 'f takes 1 argument, got 2', 2, 1);
  fails('fn f() { }\nf(1)', 'f takes 0 arguments, got 1', 2, 1);
  fails('fn f(a) { return f() }', 'f takes 1 argument, got 0', 1, 18);
  fails('f(1, x)\nfn f(a) { }', 'f takes 1 argument, got 2', 1, 1);
  run('print()\nprint(1, 2, 3)');
});

test('definitions: duplicates, builtins, repeated parameters', () => {
  fails('fn f() { }\nfn f() { }', 'duplicate function f', 2, 4);
  fails('fn f() { }\nfn g() { }\nfn f(a) { }', 'duplicate function f', 3, 4);
  fails('fn print() { }', 'print is a builtin', 1, 4);
  fails('fn f(a, b, a) { }', 'a is already declared', 1, 12);
  fails('fn f(a) { let a = 1 }', 'a is already declared', 1, 15);
  fails('fn f(a) { for a in 0..1 { } }', 'a is already declared', 1, 15);
  run('fn f(print) { return print }\nlet f = 1');
});

test('return needs a function', () => {
  fails('return', 'return outside a function', 1, 1);
  fails('print(1)\nif true { return 1 }', 'return outside a function', 2, 11);
  fails('while true { return }', 'return outside a function', 1, 14);
  run('fn f() { while true { if true { return 1 } } }');
});

test('a function sees its parameters and variables, not the top level', () => {
  const msg = (n: string) => `${n} is a top-level variable; functions see only their parameters and their own variables`;
  fails('let x = 1\nfn f() { return x }', msg('x'), 2, 17);
  fails('let x = 1\nfn f() { x = 2 }', msg('x'), 2, 10);
  fails('let x = 1\nfn f() { x += 2 }', msg('x'), 2, 10);
  fails('fn f() { return x }\nlet x = 1', msg('x'), 1, 17);
  fails('for i in 0..1 { let t = i }\nfn f() { return t }', msg('t'), 2, 17);
  fails('for i in 0..1 { }\nfn f() { return i }', msg('i'), 2, 17);
  fails('fn f() { return y }', 'unknown variable y', 1, 17);
  run('let x = 1\nfn f(x) { let y = x\n return y }\nfn g() { let x = 2\n return x }');
});

test('break and continue count loops of their own function', () => {
  fails('fn f() { break }\nwhile true { f() }', 'break outside a loop', 1, 10);
  fails('fn f() { while true { }; break }', 'break outside a loop', 1, 26);
});

test('a function used as a value is not a value, wherever it is', () => {
  fails('fn f() { }\nprint(f)', 'functions are not values', 2, 7);
  fails('fn f() { }\nlet g = f', 'functions are not values', 2, 9);
  fails('fn f() { }\nfn g() { return f }', 'functions are not values', 2, 17);
  fails('fn f() { }\nf = 1', 'functions are not values', 2, 1);
  run('fn f() { }\nlet f = 1\nprint(f)');
});

test('errors are reported in source order across functions and top-level code', () => {
  fails('print(a)\nfn f() { return b }', 'unknown variable a', 1, 7);
  fails('fn f() { return b }\nprint(a)', 'unknown variable b', 1, 17);
  fails('fn f() { }\nfn f() { }\nprint(a)', 'duplicate function f', 2, 4);
});

test('the first error in source order is the one reported', () => {
  fails('print(a)\nprint(b)\nbreak', 'unknown variable a', 1, 7);
  fails('break\nprint(b)', 'break outside a loop', 1, 1);
  fails('let x = 1\nlet x = y', 'x is already declared', 2, 5);
});

test('the string builtins resolve, with their arities', () => {
  run('print(str(1), len("a"), int("1"), lower("A"), upper("a"), slice("abc", 0, 1), read())\nfail("x")');
  fails('print(len())', 'len takes 1 argument, got 0', 1, 7);
  fails('print(str(1, 2))', 'str takes 1 argument, got 2', 1, 7);
  fails('print(slice("a", 1))', 'slice takes 3 arguments, got 2', 1, 7);
  fails('print(read(1))', 'read takes 0 arguments, got 1', 1, 7);
  fails('fail()', 'fail takes 1 argument, got 0', 1, 1);
});

test('a function cannot take a builtin\'s name, now that the builtin exists', () => {
  for (const name of ['str', 'len', 'int', 'lower', 'upper', 'slice', 'read', 'fail']) {
    fails(`fn ${name}() { }`, `${name} is a builtin`, 1, 4);
  }
  run('let len = 1\nprint(len)');
  fails('let f = len', 'functions are not values', 1, 9);
});

test('names inside an interpolation and an index are resolved, in source order', () => {
  const p = run('let s = "ab"\nprint("{s}", s[0])') as any;
  const [str, idx] = p.body[1].expr.args;
  assert.equal(str.parts[0].expr.cname, 'v_s');
  assert.equal(idx.target.cname, 'v_s');
  fails('print("a{x}b{y}")', 'unknown variable x', 1, 10);
  fails('print(y[x])', 'unknown variable y', 1, 7);
  fails('let s = "a"\nprint(s[x])', 'unknown variable x', 2, 9);
  fails('print("{nope(1)}")', 'unknown function nope', 1, 9);
  fails('print(1 in x)', 'unknown variable x', 1, 12);
  fails('fn f() { return "{t}" }\nlet t = 1', 't is a top-level variable; functions see only their parameters and their own variables', 1, 19);
});

test('an index expression is not a statement', () => {
  fails('let s = "a"\ns[0]', 'expression statement must be a call', 2, 1);
  fails('"hi"', 'expression statement must be a call', 1, 1);
});
