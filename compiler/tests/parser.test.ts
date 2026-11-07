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
  parseError('print\nx', "expected '(', found newline", 1, 6);
  parseError('print', "expected '(', found end of file", 1, 6);
  parseError('print(1', "expected ')', found end of file", 1, 8);
  parseError('print(,)', "expected an expression, found ','", 1, 7);
  parseError('print(1,,)', "expected an expression, found ','", 1, 9);
  parseError('print("hi")', 'expected an expression, found string', 1, 7);
  // Until variables (step 2) a name can only start a call.
  parseError('print(print)', "expected '(', found ')'", 1, 12);
  parseError('print(\n\n', 'expected an expression, found end of file', 3, 1);
  parseError('else', "expected a statement, found 'else'", 1, 1);
  parseError('print(1)\n}', "expected a statement, found '}'", 2, 1);
  parseError('foo bar', "expected '(', found 'bar'", 1, 5);
  parseError('"s"', 'expected a statement, found string', 1, 1);
});

// A compact s-expression of an expression, to check the shape precedence gives.
function sx(e: any): string {
  switch (e.kind) {
    case 'int': return String(e.value);
    case 'bool': return String(e.value);
    case 'nil': return 'nil';
    case 'unary': return `(${e.op} ${sx(e.operand)})`;
    case 'binary': case 'logic': return `(${e.op} ${sx(e.left)} ${sx(e.right)})`;
    case 'call': return `${e.name}(${e.args.map(sx).join(' ')})`;
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
