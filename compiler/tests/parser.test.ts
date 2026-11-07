import { test } from 'node:test';
import assert from 'node:assert/strict';
import { lex } from '../src/lexer.ts';
import { parse } from '../src/parser.ts';

const ast = (src: string) => parse(lex(src));
const at = (line: number, col: number) => ({ line, col });

function parseError(src: string, message: string, line: number, col: number) {
  assert.throws(
    () => ast(src),
    (e: any) => e.message === message && e.pos.line === line && e.pos.col === col,
    `${JSON.stringify(src)}: expected ${message} at ${line}:${col}`,
  );
}

const call = (name: string, pos: any, args: any[]) => ({
  kind: 'exprStmt',
  pos,
  expr: { kind: 'call', pos, name, args },
});
const int = (value: bigint, pos: any) => ({ kind: 'int', pos, value });

test('an empty program', () => {
  assert.deepEqual(ast(''), { kind: 'program', body: [] });
  assert.deepEqual(ast('\n// c\n;\n'), { kind: 'program', body: [] });
});

test('a call with an int argument', () => {
  assert.deepEqual(ast('print(42)').body, [call('print', at(1, 1), [int(42n, at(1, 7))])]);
});

test('calls with no, one and several arguments', () => {
  assert.deepEqual(ast('print()').body, [call('print', at(1, 1), [])]);
  assert.deepEqual(ast('print(1, 2_0)').body, [
    call('print', at(1, 1), [int(1n, at(1, 7)), int(20n, at(1, 10))]),
  ]);
});

test('statements end at newlines and semicolons; blanks are skipped', () => {
  const b = ast('print(1);print(2)\n\n;print(3);\n').body;
  assert.deepEqual(b.map((s: any) => s.expr.args[0].value), [1n, 2n, 3n]);
  assert.deepEqual(b.map((s: any) => s.pos.line), [1, 1, 3]);
});

test('a call may break across lines and end with a comma', () => {
  const b = ast('print(\n1,\n2,\n)\n').body;
  assert.deepEqual(b[0].expr.args.map((a: any) => a.value), [1n, 2n]);
});

test('errors: expected X, found Y', () => {
  parseError('print(1 2)', "expected ')', found '2'", 1, 9);
  parseError('print(1) print(2)', "expected newline, found 'print'", 1, 10);
  parseError('print(1', "expected ')', found end of file", 1, 8);
  parseError('print(,)', "expected an expression, found ','", 1, 7);
  parseError('print(1,,)', "expected an expression, found ','", 1, 9);
  parseError('print(\n\n', 'expected an expression, found end of file', 3, 1);
  parseError('else', "expected a statement, found 'else'", 1, 1);
  parseError('print(1)\n}', "expected a statement, found '}'", 2, 1);
  parseError('foo bar', 'expected newline, found \'bar\'', 1, 5);
});

// A compact s-expression of an expression, to check the shape precedence gives.
function sx(e: any): string {
  switch (e.kind) {
    case 'int': return String(e.value);
    case 'bool': return String(e.value);
    case 'nil': return 'nil';
    case 'unary': return `(${e.op} ${sx(e.operand)})`;
    case 'binary': case 'logic': return `(${e.op} ${sx(e.left)} ${sx(e.right)})`;
    case 'name': return e.name;
    case 'call': return `${e.name}(${e.args.map(sx).join(' ')})`;
    case 'index': return `${sx(e.target)}[${sx(e.index)}]`;
    case 'list': return `[${e.items.map(sx).join(' ')}]`;
    case 'map': return `{${e.entries.map((x: any) => `${sx(x.key)}:${sx(x.value)}`).join(' ')}}`;
    case 'field': return `${sx(e.target)}.${e.name}`;
    case 'string':
      return '"' + e.parts.map((q: any) => (q.kind === 'text' ? q.value : `{${sx(q.expr)}}`)).join('') + '"';
  }
  throw new Error(e.kind);
}
const shape = (src: string) => sx((ast(`print(${src})`).body[0] as any).expr.args[0]);

test('precedence, loosest to tightest', () => {
  assert.equal(shape('1 or 2 and 3'), '(or 1 (and 2 3))');
  assert.equal(shape('not 1 == 2'), '(not (== 1 2))');
  assert.equal(shape('not not true'), '(not (not true))');
  assert.equal(shape('1 + 2 < 3 * 4'), '(< (+ 1 2) (* 3 4))');
  assert.equal(shape('1 + 2 * 3'), '(+ 1 (* 2 3))');
  assert.equal(shape('-1 * 2'), '(* (- 1) 2)');
  assert.equal(shape('- -1'), '(- (- 1))');
  assert.equal(shape('1 == 2 and 3 != 4 or nil'), '(or (and (== 1 2) (!= 3 4)) nil)');
  assert.equal(shape('not 1 < 2 and 3 > 4'), '(and (not (< 1 2)) (> 3 4))');
});

test('binary operators associate to the left; parentheses group', () => {
  assert.equal(shape('1 - 2 - 3'), '(- (- 1 2) 3)');
  assert.equal(shape('8 / 4 / 2 % 3'), '(% (/ (/ 8 4) 2) 3)');
  assert.equal(shape('true and false and nil'), '(and (and true false) nil)');
  assert.equal(shape('1 - (2 - 3)'), '(- 1 (- 2 3))');
  assert.equal(shape('((1))'), '1');
});

test('operator nodes are positioned at the operator', () => {
  const e = (ast('print(1 + 2)').body[0] as any).expr.args[0];
  assert.deepEqual(e.pos, at(1, 9));
  const n = (ast('print(not true)').body[0] as any).expr.args[0];
  assert.deepEqual(n.pos, at(1, 7));
});

test('a newline after a binary operator continues the expression', () => {
  // At statement level, where the lexer doesn't drop newlines itself.
  const b = ast('1 +\n\n 2 and\n true\n3').body as any[];
  assert.equal(b.length, 2);
  assert.equal(sx(b[0].expr), '(and (+ 1 2) true)');
  assert.deepEqual(b[0].pos, at(1, 1));
});

test('comparisons do not chain, at the second operator', () => {
  parseError('print(1 < 2 < 3)', 'comparisons do not chain', 1, 13);
  parseError('print(1 == 2 == 3)', 'comparisons do not chain', 1, 14);
  parseError('print(1 < 2 != 3)', 'comparisons do not chain', 1, 13);
  assert.equal(shape('(1 < 2) == true'), '(== (< 1 2) true)');
});

test('operand errors', () => {
  parseError('print(1 +)', "expected an expression, found ')'", 1, 10);
  parseError('print(not)', "expected an expression, found ')'", 1, 10);
  parseError('1 -\n', 'expected an expression, found end of file', 2, 1);
  parseError('-\n1', "expected an expression, found newline", 1, 2);
  parseError('print((1)', "expected ')', found end of file", 1, 10);
  parseError('print(1 and or 2)', "expected an expression, found 'or'", 1, 13);
});

test('a statement may be any expression; the resolver judges it', () => {
  const b = ast('42\n-1\ntrue\nnot nil\n(1)\n').body as any[];
  assert.deepEqual(b.map((s) => s.expr.kind), ['int', 'unary', 'bool', 'unary', 'int']);
  assert.deepEqual(b.map((s) => s.pos.line), [1, 2, 3, 4, 5]);
});

// Step 2: variables and control flow.

test('a name in an expression is a name node; a call is still a call', () => {
  assert.equal(shape('x + f(y)'), '(+ x f(y))');
  const e = (ast('print(abc)').body[0] as any).expr.args[0];
  assert.deepEqual(e, { kind: 'name', pos: at(1, 7), name: 'abc' });
});

test('let: the name, its position and the value', () => {
  const s = ast('  let total = 1 +\n 2').body[0] as any;
  assert.equal(s.kind, 'let');
  assert.deepEqual(s.pos, at(1, 3));
  assert.equal(s.name, 'total');
  assert.deepEqual(s.namePos, at(1, 7));
  assert.equal(sx(s.value), '(+ 1 2)');
});

test('assignment: target, operator position, value', () => {
  const b = ast('x = 1\n  y += 2 * 3\nz %= 4').body as any[];
  assert.deepEqual(b.map((s) => s.kind), ['assign', 'assign', 'assign']);
  assert.deepEqual(b.map((s) => s.op), ['=', '+=', '%=']);
  assert.deepEqual(b.map((s) => s.pos), [at(1, 3), at(2, 5), at(3, 3)]);
  // The target is a variable and a list of steps (paths arrive in step 5).
  assert.deepEqual(b[1].target, { kind: 'target', pos: at(2, 3), name: 'y', steps: [] });
  assert.equal(sx(b[1].value), '(* 2 3)');
  const t = ast('x =\n\n  5').body[0] as any;
  assert.equal(t.value.value, 5n);
});

test('every compound operator parses', () => {
  const ops = ['+=', '-=', '*=', '/=', '%='];
  const b = ast(ops.map((o) => `x ${o} 1`).join('\n')).body as any[];
  assert.deepEqual(b.map((s) => s.op), ops);
});

test('cannot assign to this, at the first token of the target', () => {
  parseError('1 = 2', 'cannot assign to this', 1, 1);
  parseError('print(1) = 2', 'cannot assign to this', 1, 1);
  parseError('  x + 1 = 2', 'cannot assign to this', 1, 3);
  parseError('-x += 2', 'cannot assign to this', 1, 1);
  parseError('(x + 1) *= 2', 'cannot assign to this', 1, 1);
  parseError('true = false', 'cannot assign to this', 1, 1);
});

test('if / else if / else, with else on the next line', () => {
  const s = ast('if a {\n}\nelse if b {\n  print(1)\n}\n\nelse {\n}\nprint(2)').body as any[];
  assert.equal(s.length, 2);
  assert.equal(s[0].kind, 'if');
  assert.deepEqual(s[0].condPos, at(1, 4));
  assert.equal(s[0].else.length, 1);
  assert.equal(s[0].else[0].kind, 'if');
  assert.deepEqual(s[0].else[0].else, []);
  assert.equal(s[0].else[0].then.length, 1);
  assert.equal(s[1].kind, 'exprStmt');
  const none = ast('if a { print(1) }').body[0] as any;
  assert.equal(none.else, null);
});

test('the condition position is its first token, not its operator', () => {
  const w = ast('while  1 + 2 < 3 {\n}').body[0] as any;
  assert.equal(w.kind, 'while');
  assert.deepEqual(w.condPos, at(1, 8));
  assert.deepEqual(w.cond.pos, at(1, 14));
});

test('for over a range, half-open and inclusive, and over a value', () => {
  const r = ast('for i in 0..n + 1 {\n}').body[0] as any;
  assert.equal(r.kind, 'for');
  assert.equal(r.name, 'i');
  assert.deepEqual(r.namePos, at(1, 5));
  assert.equal(r.iter.kind, 'range');
  assert.equal(r.iter.inclusive, false);
  assert.deepEqual([r.iter.loPos, r.iter.hiPos], [at(1, 10), at(1, 13)]);
  assert.equal(sx(r.iter.hi), '(+ n 1)');
  const q = ast('for i in 1..=5 { print(i) }').body[0] as any;
  assert.equal(q.iter.inclusive, true);
  assert.equal(q.body.length, 1);
  const e = ast('for x in  y + 1 {\n}').body[0] as any;
  assert.equal(e.iter.kind, 'each');
  assert.deepEqual(e.iter.exprPos, at(1, 11));
});

test('break and continue; blocks hold statements separated by newlines or ;', () => {
  const w = ast('while true { break; continue\n  print(1) }').body[0] as any;
  assert.deepEqual(w.body.map((s: any) => s.kind), ['break', 'continue', 'exprStmt']);
  assert.deepEqual(w.body[1].pos, at(1, 21));
  assert.deepEqual((ast('while true {}').body[0] as any).body, []);
});

test('step 2 parse errors', () => {
  parseError('let 5 = 1', "expected a name, found '5'", 1, 5);
  parseError('let x 5', "expected '=', found '5'", 1, 7);
  parseError('let x', "expected '=', found end of file", 1, 6);
  parseError('let x =', 'expected an expression, found end of file', 1, 8);
  parseError('if true\n{', "expected '{', found newline", 1, 8);
  parseError('if true {\n  print(1)\n', "expected '}', found end of file", 3, 1);
  parseError('if true { print(1) } print(2)', "expected newline, found 'print'", 1, 22);
  parseError('if true {\n} else print(1)', "expected '{', found 'print'", 2, 8);
  parseError('for i 0..3 {\n}', "expected 'in', found '0'", 1, 7);
  parseError('for 1 in 2..3 {\n}', "expected a name, found '1'", 1, 5);
  parseError('while ) {\n}', "expected an expression, found ')'", 1, 7);
  parseError('print(1..2)', "expected ')', found '..'", 1, 8);
  parseError('else {', "expected a statement, found 'else'", 1, 1);
  parseError('fn', 'expected a name, found end of file', 1, 3);
});

// Step 3: functions.
test('fn parses a name, parameters and a body; return is bare or has a value', () => {
  const p = ast('fn gcd(a, b) {\n  return a\n}\nfn none() { return }').body as any[];
  assert.equal(p[0].kind, 'fn');
  assert.deepEqual(p[0].pos, at(1, 1));
  assert.equal(p[0].name, 'gcd');
  assert.deepEqual(p[0].namePos, at(1, 4));
  assert.deepEqual(p[0].params.map((x: any) => [x.name, x.pos.col]), [['a', 8], ['b', 11]]);
  assert.equal(p[0].body[0].kind, 'return');
  assert.deepEqual(p[0].body[0].pos, at(2, 3));
  assert.equal(sx(p[0].body[0].value), 'a');
  assert.deepEqual(p[1].params, []);
  assert.equal(p[1].body[0].value, null);
});

test('a bare return ends at a newline, a semicolon or a brace', () => {
  for (const src of ['fn f() { return }', 'fn f() { return; }', 'fn f() {\n return\n}']) {
    assert.equal((ast(src).body[0] as any).body[0].value, null, src);
  }
  assert.equal(sx((ast('fn f() { return 1 + 2 }').body[0] as any).body[0].value), '(+ 1 2)');
});

test('parameters and arguments may end with a comma and break across lines', () => {
  const p = ast('fn f(\n a,\n b,\n) { }\nprint(f(\n1,\n2,\n))').body as any[];
  assert.deepEqual(p[0].params.map((x: any) => x.name), ['a', 'b']);
});

test('a call to a user function parses like any call', () => {
  const e = (ast('print(gcd(1, 2))').body[0] as any).expr.args[0];
  assert.equal(sx(e), 'gcd(1 2)');
});

test('fn is a top-level statement only', () => {
  parseError('fn f() {\n  fn g() { }\n}', 'functions are defined at the top level', 2, 3);
  parseError('if true {\n  fn g() { }\n}', 'functions are defined at the top level', 2, 3);
  parseError('while true { fn g() { } }', 'functions are defined at the top level', 1, 14);
  // The error is the keyword's, before anything after it is read.
  parseError('if true { fn }', 'functions are defined at the top level', 1, 11);
});

test('step 3 parse errors', () => {
  parseError('fn 1() { }', "expected a name, found '1'", 1, 4);
  parseError('fn if() { }', "expected a name, found 'if'", 1, 4);
  parseError('fn f { }', "expected '(', found '{'", 1, 6);
  parseError('fn f(1) { }', "expected a name, found '1'", 1, 6);
  parseError('fn f(a b) { }', "expected ')', found 'b'", 1, 8);
  parseError('fn f(a,,) { }', "expected a name, found ','", 1, 8);
  parseError('fn f()\n{ }', "expected '{', found newline", 1, 7);
  parseError('fn f() {\n return 1\n', "expected '}', found end of file", 3, 1);
  parseError('fn f() { return ) }', "expected an expression, found ')'", 1, 17);
  parseError('fn f() { } fn g() { }', "expected newline, found 'fn'", 1, 12);
});

test('a string literal is text and interpolated expressions, in order', () => {
  const e = (ast('print("a{x + 1}b{y}")').body[0] as any).expr.args[0];
  assert.equal(e.kind, 'string');
  assert.deepEqual(e.pos, at(1, 7));
  assert.equal(sx(e), '"a{(+ x 1)}b{y}"');
  assert.deepEqual(e.parts[1].pos, at(1, 9));
  assert.deepEqual(e.parts[1].expr.pos, at(1, 12)); // the `+`, where faults point
  assert.equal(sx((ast('print("")').body[0] as any).expr.args[0]), '""');
});

test('an interpolation holds any expression, including strings and calls', () => {
  assert.equal(shape('"{f("x{y}")}"'), '"{f("x{y}")}"');
  assert.equal(shape('"{a[0]}{-b}{not c}"'), '"{a[0]}{(- b)}{(not c)}"');
});

test('indexing binds tighter than prefix minus and applies to calls, strings and parentheses', () => {
  assert.equal(shape('-s[0]'), '(- s[0])');
  assert.equal(shape('s[0][1]'), 's[0][1]');
  assert.equal(shape('f(1)[2]'), 'f(1)[2]');
  assert.equal(shape('"abc"[1 + 1]'), '"abc"[(+ 1 1)]');
  assert.equal(shape('(a + b)[0] * 2'), '(* (+ a b)[0] 2)');
  const e = (ast('print(s [\n 1\n ])').body[0] as any).expr.args[0];
  assert.deepEqual(e.pos, at(1, 9)); // the `[`
});

test('in and not in are comparisons: below + and above and/not, not chained', () => {
  assert.equal(shape('a + b in c + d'), '(in (+ a b) (+ c d))');
  assert.equal(shape('a not in b'), '(not in a b)');
  assert.equal(shape('not a in b'), '(not (in a b))');
  assert.equal(shape('a in b and c not in d'), '(and (in a b) (not in c d))');
  const bin = (src: string) => (ast(`print(${src})`).body[0] as any).expr.args[0];
  assert.deepEqual(bin('a in b').pos, at(1, 9));
  assert.deepEqual(bin('a not in b').pos, at(1, 9)); // the `not`
  parseError('print(a in b in c)', 'comparisons do not chain', 1, 14);
  parseError('print(a < b in c)', 'comparisons do not chain', 1, 13);
  parseError('print(a in b not in c)', 'comparisons do not chain', 1, 14);
  parseError('print(a == b not in c)', 'comparisons do not chain', 1, 14);
});

test('a for header may iterate over an in-less expression: for c in s', () => {
  const f = ast('for c in "ab" + s {\n}').body[0] as any;
  assert.equal(f.iter.kind, 'each');
  assert.equal(sx(f.iter.expr), '(+ "ab" s)');
});

test('step 4 parse errors', () => {
  parseError('print("{1 2}")', "expected '}', found '2'", 1, 11);
  parseError('print("{1 +}")', "expected an expression, found '}'", 1, 12);
  parseError('print("{)}")', "expected an expression, found ')'", 1, 9);
  parseError('print(s[0)', "expected ']', found ')'", 1, 10);
  parseError('print(s[])', "expected an expression, found ']'", 1, 9);
  parseError('print("a" "b")', "expected ')', found string", 1, 11);
  parseError('print(a not b)', "expected ')', found 'not'", 1, 9);
});

test('a list literal: items, trailing comma, nesting, breaks across lines, the position of its [', () => {
  const lst = (src: string) => (ast(`print(${src})`).body[0] as any).expr.args[0];
  assert.equal(sx(lst('[]')), '[]');
  assert.equal(sx(lst('[1, 2, 3]')), '[1 2 3]');
  assert.equal(sx(lst('[1, 2,]')), '[1 2]');
  assert.equal(sx(lst('[[1], [], [[2]]]')), '[[1] [] [[2]]]');
  assert.equal(sx(lst('[\n  1 +\n 2,\n  "a",\n]')), '[(+ 1 2) "a"]');
  assert.equal(sx(lst('[1 < 2, not true, -3, f(1)]')), '[(< 1 2) (not true) (- 3) f(1)]');
  assert.deepEqual(lst('  [1]').pos, at(1, 9));
});

test('indexing after a list literal, a call and a parenthesized expression', () => {
  const idx = (src: string) => (ast(`print(${src})`).body[0] as any).expr.args[0];
  assert.equal(idx('[1, 2][0]').kind, 'index');
  assert.equal(idx('[1, 2][0]').target.kind, 'list');
  assert.equal(idx('[[1]][0][0]').target.kind, 'index');
  assert.equal(idx('f(x)[1]').target.kind, 'call');
  assert.equal(idx('(xs)[1]').target.kind, 'name');
  assert.deepEqual(idx('[1][0]').pos, at(1, 10));
});

test('an assignment target is a name and any number of [index] steps', () => {
  const b = ast('xs[0] = 1\ng[i + 1][j] += 2\nys[ys[0]][1][2] -= 3\n(zs)[4] *= 5').body as any[];
  assert.deepEqual(b.map((s) => s.kind), ['assign', 'assign', 'assign', 'assign']);
  assert.deepEqual(b.map((s) => s.target.name), ['xs', 'g', 'ys', 'zs']);
  assert.deepEqual(b.map((s) => s.target.steps.length), [1, 2, 3, 1]);
  assert.deepEqual(b.map((s) => s.op), ['=', '+=', '-=', '*=']);
  // The statement's pos is its operator; the target's is the first token; a step's is its `[`.
  assert.deepEqual(b[0].pos, at(1, 7));
  assert.deepEqual(b[0].target.pos, at(1, 1));
  assert.deepEqual(b[0].target.steps[0], { kind: 'index', pos: at(1, 3), index: { kind: 'int', pos: at(1, 4), value: 0n } });
  assert.deepEqual(b[1].target.steps.map((s: any) => s.pos), [at(2, 2), at(2, 9)]);
  assert.equal(sx(b[1].target.steps[0].index), '(+ i 1)');
  assert.equal(sx(b[2].target.steps[0].index), 'ys[0]');
  assert.deepEqual(b[3].target.pos, at(4, 1));
});

test('cannot assign to this: a path must start at a name and have only index steps', () => {
  parseError('[1, 2][0] = 5', 'cannot assign to this', 1, 1);
  parseError('f(x)[0] = 1', 'cannot assign to this', 1, 1);
  parseError('"abc"[0] = "x"', 'cannot assign to this', 1, 1);
  parseError('  (xs[0] + 1)[0] = 1', 'cannot assign to this', 1, 3);
  parseError('[1] += [2]', 'cannot assign to this', 1, 1);
  parseError('xs\n[0] = 1', 'cannot assign to this', 2, 1);
});

test('list literal errors', () => {
  parseError('print([1 2])', "expected ']', found '2'", 1, 10);
  parseError('print([,])', "expected an expression, found ','", 1, 8);
  parseError('print([1,,2])', "expected an expression, found ','", 1, 10);
  parseError('print([1,', 'expected an expression, found end of file', 1, 10);
  parseError('let xs = [1, 2\nprint(xs)', "expected ']', found 'print'", 2, 1);
  parseError('print(1])', "expected ')', found ']'", 1, 8);
});

// Step 6: maps.
const mapOf = (src: string) => (ast(`print(${src})`).body[0] as any).expr.args[0];

test('a map literal: key forms, trailing comma, nesting, any layout, the position of its {', () => {
  assert.equal(sx(mapOf('{}')), '{}');
  assert.equal(sx(mapOf('{a: 1, "b": 2, 3: 4, -5: 6}')), '{"a":1 "b":2 3:4 -5:6}');
  assert.equal(sx(mapOf('{a: 1,}')), '{"a":1}');
  assert.equal(sx(mapOf('{a: {b: [1, {c: 2}]}}')), '{"a":{"b":[1 {"c":2}]}}');
  assert.equal(sx(mapOf('{1_0: 1, 007: 2}')), '{10:1 7:2}');
  assert.equal(sx(mapOf('{x: 1 + 2 * 3, y: not true, z: f(1)}')), '{"x":(+ 1 (* 2 3)) "y":(not true) "z":f(1)}');
  assert.equal(sx(mapOf('{in2: 1, len: 2, print: 3}')), '{"in2":1 "len":2 "print":3}');
  assert.deepEqual(mapOf('  {a: 1}').pos, at(1, 9));
  // A key is its own literal node at its own first token: a name is a string.
  const e = mapOf('{a: 1, "b": 2, -3: 4}');
  assert.deepEqual(e.entries.map((x: any) => [x.key.kind, x.key.pos]), [['string', at(1, 8)], ['string', at(1, 14)], ['int', at(1, 22)]]);
  assert.deepEqual(e.entries[0].key.parts, [{ kind: 'text', value: 'a' }]);
  assert.equal(e.entries[2].key.value, -3n);
});

test('newlines are ignored anywhere inside a map literal', () => {
  const src = 'let m = {\n  a\n  :\n  1\n\n  ,\n  b: 2 +\n  3\n  ,\n}\nprint(m)';
  const b = ast(src).body as any[];
  assert.equal(b.length, 2);
  assert.equal(sx(b[0].value), '{"a":1 "b":(+ 2 3)}');
  assert.equal(sx(mapOf('{\n}')), '{}');
  assert.equal(sx(mapOf('{a: {\n b: 1\n }\n, c: 2}')), '{"a":{"b":1} "c":2}');
});

test('a field: .name after any postfix, binding tighter than prefix minus', () => {
  const sh = (src: string) => sx(mapOf(src));
  assert.equal(sh('m.a'), 'm.a');
  assert.equal(sh('m.a.b.c'), 'm.a.b.c');
  assert.equal(sh('m.a[1].b'), 'm.a[1].b');
  assert.equal(sh('-m.a * 2'), '(* (- m.a) 2)');
  assert.equal(sh('f(1).x'), 'f(1).x');
  assert.equal(sh('(m).x'), 'm.x');
  assert.equal(sh('{a: 1}.a'), '{"a":1}.a');
  assert.equal(sh('[{a: 1}][0].a'), '[{"a":1}][0].a');
  assert.equal(sh('"s".len'), '"s".len');
  assert.equal(sh('m.if2'), 'm.if2');
  // A field's position is its `.`; a statement may start with a name and a field step.
  assert.deepEqual(mapOf('m.a').pos, at(1, 8));
  assert.equal(mapOf('m.a').name, 'a');
});

test('an assignment target mixes index and field steps', () => {
  const b = ast('m.a = 1\nm.a[0].b["c"] += 2\ndb[i].x.y -= 3').body as any[];
  assert.deepEqual(b.map((s) => s.target.steps.map((st: any) => st.kind)), [['field'], ['field', 'index', 'field', 'index'], ['index', 'field', 'field']]);
  assert.deepEqual(b[0].target.steps[0], { kind: 'field', pos: at(1, 2), name: 'a' });
  assert.deepEqual(b[1].target.steps.map((st: any) => st.pos), [at(2, 2), at(2, 4), at(2, 7), at(2, 9)]);
  assert.deepEqual(b[2].target.steps.map((st: any) => st.name), [undefined, 'x', 'y']);
});

test('cannot assign to this: a field of a call or a literal', () => {
  parseError('f().x = 1', 'cannot assign to this', 1, 1);
  parseError('(m.a + 1).b = 1', 'cannot assign to this', 1, 1);
  parseError('m.a().b = 1', 'expected newline, found \'(\'', 1, 4);
});

test('map literal and field errors', () => {
  const key = 'map key must be a name, a string or an int';
  parseError('print({[1]: 2})', key, 1, 8);
  parseError('print({true: 1})', key, 1, 8);
  parseError('print({a: 1, nil: 2})', key, 1, 14);
  parseError('print({(1): 2})', key, 1, 8);
  parseError('print({"a{x}": 1})', key, 1, 8);
  parseError('print({-a: 1})', key, 1, 8);
  parseError('print({--1: 1})', key, 1, 8);
  parseError('print({a: 1,, b: 2})', key, 1, 13);
  parseError('print({, a: 1})', key, 1, 8);
  parseError('print({1 + 2: 3})', "expected ':', found '+'", 1, 10);
  parseError('print({f(): 1})', "expected ':', found '('", 1, 9);
  parseError('print({a 1})', "expected ':', found '1'", 1, 10);
  parseError('print({a: })', "expected an expression, found '}'", 1, 11);
  parseError('print({a: 1 b: 2})', "expected '}', found 'b'", 1, 13);
  parseError('let m = {a: 1\n', "expected '}', found end of file", 2, 1);
  parseError('print(m.)', "expected a name, found ')'", 1, 9);
  parseError('print(m.1)', "expected a name, found '1'", 1, 9);
  parseError('print(m.in)', "expected a name, found 'in'", 1, 9);
  parseError('m.\nprint(1)', 'expected a name, found newline', 1, 3);
  // A map or a block is not a statement; a `.` does not continue the line before.
  parseError('{a: 1}', "expected a statement, found '{'", 1, 1);
  parseError('{ let x = 1 }', "expected a statement, found '{'", 1, 1);
  parseError('m\n.a = 1', "expected a statement, found '.'", 2, 1);
});

test('a map literal after a condition or a loop header is a value, and the block follows', () => {
  const b = ast('if m == {} {\n}\nfor k in {a: 1} {\n}\nwhile {} != m {\n}').body as any[];
  assert.equal(sx(b[0].cond), '(== m {})');
  assert.equal(sx(b[1].iter.expr), '{"a":1}');
  assert.equal(sx(b[2].cond), '(!= {} m)');
});
