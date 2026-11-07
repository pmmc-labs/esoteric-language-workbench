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
  parseError('print(print)', "expected an expression, found 'print'", 1, 7);
  parseError('print(\n\n', 'expected an expression, found end of file', 3, 1);
  parseError('42', "expected a statement, found '42'", 1, 1);
  parseError('else', "expected a statement, found 'else'", 1, 1);
  parseError('print(1)\n}', "expected a statement, found '}'", 2, 1);
  parseError('foo bar', "expected '(', found 'bar'", 1, 5);
  parseError('1_000', "expected a statement, found '1_000'", 1, 1);
  parseError('"s"', 'expected a statement, found string', 1, 1);
});
