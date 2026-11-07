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

test("a let in a block is visible to the end of the block, then gone (D14, D38)", () => {
  resolve(parse(lex("if 1 { let a = 2\nprint a }\nprint 3")));
  assert.deepEqual(err("if 1 { let a = 2 }\nprint a"), { line: 2, col: 7, msg: "unknown variable a" });
  assert.deepEqual(err("while 0 { let a = 2 }\nlet b = a"), { line: 2, col: 9, msg: "unknown variable a" });
});

test("names from enclosing blocks are visible inside, and can be written", () => {
  resolve(parse(lex("let a = 1\nif a = 1 { a <- 2\nif 1 { print a } }")));
  resolve(parse(lex("if 1 { let a = 1 if 1 { print a } }")));
});

test("redeclaring a name visible from an enclosing block is an error, at the inner name", () => {
  assert.deepEqual(err("let a = 1\nwhile 0 {\n  let a = 2\n}"), { line: 3, col: 7, msg: "a is already declared" });
  assert.deepEqual(err("if 1 { let a = 1 if 1 { let a = 2 } }"), { line: 1, col: 29, msg: "a is already declared" });
});

test("sibling blocks and later outer lets may reuse a finished block's name", () => {
  resolve(parse(lex("if 1 { let a = 1 } else { let a = 2 }\nif 1 { let a = 3 }\nlet a = 4\nprint a")));
});

test("a condition is resolved outside its block; an else if has its own scope", () => {
  assert.deepEqual(err("while x { let x = 1 }"), { line: 1, col: 7, msg: "unknown variable x" });
  assert.deepEqual(err("if 0 { let a = 1 } else if a { }"), { line: 1, col: 28, msg: "unknown variable a" });
});
