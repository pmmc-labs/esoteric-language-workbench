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

test("function errors, each at the name (D24, D39)", () => {
  assert.deepEqual(err("print f(1)"), { line: 1, col: 7, msg: "unknown function f" });
  assert.deepEqual(err("f(1)"), { line: 1, col: 1, msg: "unknown function f" });
  assert.deepEqual(err("fn f() { }\nfn f() { }"), { line: 2, col: 4, msg: "f is already defined" });
  for (const b of ["len", "at", "str"]) {
    assert.deepEqual(err(`fn ${b}() { }`), { line: 1, col: 4, msg: `${b} is a builtin` });
  }
  assert.deepEqual(err("fn f(a, b) { }\nprint f(1)"),
    { line: 2, col: 7, msg: "f takes 2 arguments, given 1" });
  assert.equal(err("fn f(a) { }\nf()").msg, "f takes 1 argument, given 0");
  assert.equal(err("fn f() { }\nf(1)").msg, "f takes 0 arguments, given 1");
});

test("return outside a function, at the keyword; fine inside", () => {
  assert.deepEqual(err("print 1\nreturn 2"), { line: 2, col: 1, msg: "return outside a function" });
  assert.deepEqual(err("if 1 { return 2 }"), { line: 1, col: 8, msg: "return outside a function" });
  resolve(parse(lex("fn f() { if 1 { return 2 } }")));
});

test("a function sees its parameters and lets, not the main program's names", () => {
  assert.deepEqual(err("let x = 1\nfn f() { return x }"), { line: 2, col: 17, msg: "unknown variable x" });
  resolve(parse(lex("fn f(a) { let b = a\nreturn b }")));
  assert.equal(err("fn f(a) { let a = 1 }").msg, "a is already declared");
  assert.deepEqual(err("fn f(a, a) { }"), { line: 1, col: 9, msg: "a is already declared" });
});

test("hoisting, mutual recursion, and a function and a variable may share a name", () => {
  resolve(parse(lex("print f(1)\nfn f(n) { return g(n) }\nfn g(n) { return f(n) }")));
  resolve(parse(lex("fn f() { }\nlet f = 1\nprint f")));
});
