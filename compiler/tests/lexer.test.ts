import { test } from "node:test";
import assert from "node:assert/strict";
import { lex } from "../src/lexer.ts";

const kinds = (src: string) => lex(src).map((t) => `${t.k}:${t.text}`);
const err = (src: string) => {
  try { lex(src); } catch (e) { return e as { line: number; col: number; msg: string }; }
  assert.fail("expected a compile error");
};

test("names, keywords, integers", () => {
  assert.deepEqual(kinds("let x_1 = 42"), ["kw:let", "name:x_1", "op:=", "int:42", "eof:"]);
  for (const k of ["fn", "let", "if", "else", "while", "return", "print", "write", "and", "or", "not"]) {
    assert.equal(lex(k)[0].k, "kw");
  }
  assert.equal(lex("printx")[0].k, "name");
  assert.equal(lex("_a")[0].k, "name");
});

test("every operator and punctuation, longest first", () => {
  const ops = "<- <= >= != + - * / % = < > @ # ( ) [ ] { } ,";
  assert.deepEqual(lex(ops).slice(0, -1).map((t) => t.text), ops.split(" "));
  assert.deepEqual(kinds("a<-1"), ["name:a", "op:<-", "int:1", "eof:"]);
  assert.deepEqual(kinds("a<=b"), ["name:a", "op:<=", "name:b", "eof:"]);
  assert.deepEqual(kinds("a<b"), ["name:a", "op:<", "name:b", "eof:"]);
  assert.deepEqual(kinds("a--b"), ["name:a", "op:-", "op:-", "name:b", "eof:"]);
});

test("strings and escapes", () => {
  const t = lex('"a\\n\\t\\"\\\\b"')[0];
  assert.equal(t.k, "str");
  assert.equal(t.val, 'a\n\t"\\b');
  assert.equal(lex('""')[0].val, "");
  assert.equal(lex('"a;b"')[0].val, "a;b"); // ; inside a string isn't a comment
});

test("comments, whitespace, positions", () => {
  const toks = lex("print 1 ; c\n\r\n  print\t2");
  assert.deepEqual(toks.map((t) => [t.line, t.col]), [[1, 1], [1, 7], [3, 3], [3, 9], [3, 10]]);
  assert.equal(lex("")[0].k, "eof");
  assert.deepEqual([lex("a\n")[1].line, lex("a\n")[1].col], [2, 1]);
});

test("integer range", () => {
  assert.equal(lex("9223372036854775807")[0].val, "9223372036854775807");
  assert.deepEqual(err("print 9223372036854775808"), { line: 1, col: 7, msg: "integer literal out of range" });
  assert.equal(err("99999999999999999999999").msg, "integer literal out of range");
});

test("lexical errors", () => {
  assert.deepEqual(err("print $"), { line: 1, col: 7, msg: "unexpected character '$'" });
  assert.deepEqual(err("a !b"), { line: 1, col: 3, msg: "unexpected character '!'" });
  assert.equal(err("\x01").msg, "unexpected character '\\x01'");
  assert.equal(err("\xe9").msg, "unexpected character '\\xe9'");
  assert.deepEqual(err('x\n  "abc'), { line: 2, col: 3, msg: "unterminated string" });
  assert.equal(err('"abc\ndef"').msg, "unterminated string");
  assert.equal(err('"abc\\').msg, "unterminated string");
  assert.deepEqual(err('"a\\qb"'), { line: 1, col: 3, msg: "unknown escape \\q" });
});
