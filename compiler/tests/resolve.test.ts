import { test } from "node:test";
import assert from "node:assert/strict";
import { lex } from "../src/lexer.ts";
import { parse } from "../src/parser.ts";
import { resolve } from "../src/resolve.ts";

const err = (src: string) => {
  try { resolve(parse(lex(src))); } catch (e) { return e as { line: number; col: number; msg: string }; }
  assert.fail("expected a compile error");
};

test("unknown variable, with the name's position", () => {
  assert.deepEqual(err("print x"), { line: 1, col: 7, msg: "unknown variable x" });
  assert.deepEqual(err("let a = 1\n  b <- a"), { line: 2, col: 3, msg: "unknown variable b" });
  assert.equal(err("let a = [1, b]").msg, "unknown variable b");
  assert.equal(err("let a = 1\nprint a@c").msg, "unknown variable c");
});

test("a name is not visible in its own initializer, only after the let", () => {
  assert.deepEqual(err("let x = x"), { line: 1, col: 9, msg: "unknown variable x" });
  resolve(parse(lex("let x = 1\nlet y = x\nx <- y")));
});

test("already declared, at the second name", () => {
  assert.deepEqual(err("let a = 1\nlet a = 2"), { line: 2, col: 5, msg: "a is already declared" });
  // Source order: the redeclaration is reported before the bad initializer.
  assert.equal(err("let a = 1\nlet a = b").msg, "a is already declared");
});
