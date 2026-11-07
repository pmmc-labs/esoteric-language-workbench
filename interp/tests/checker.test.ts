import { test } from "node:test";
import assert from "node:assert/strict";
import { read } from "../src/reader.ts";
import { check } from "../src/checker.ts";
import { CheckError } from "../src/errors.ts";

// The error before running for a program, as `L:C message`, or "ok".
export const checked = (src: string) => {
  try { check(read(src)); return "ok"; } catch (e) {
    assert.ok(e instanceof CheckError, String(e));
    return `${e.line}:${e.col} ${e.message}`;
  }
};

test("arithmetic with two operands is fine", () => {
  assert.equal(checked("(+ (* 6 7) (- 10 (/ 7 2)))"), "ok");
  assert.equal(checked("(% 1 2)"), "ok");
});

test("an operator with other than two operands (D3)", () => {
  assert.equal(checked("(+ 1 2 3)"), "1:1 + takes 2 arguments, not 3");
  assert.equal(checked("(- 1)"), "1:1 - takes 2 arguments, not 1");
  assert.equal(checked("(*)"), "1:1 * takes 2 arguments, not 0");
  assert.equal(checked("(+ 1\n  (/ 1 2 3))"), "2:3 / takes 2 arguments, not 3");
});

test("an unknown name, as an operator or on its own (D7)", () => {
  assert.equal(checked("(foo 1 2)"), "1:2 unknown name foo");
  assert.equal(checked("x"), "1:1 unknown name x");
  assert.equal(checked("(+ 1 y)"), "1:6 unknown name y");
});

test("a list whose head isn't an operator", () => {
  assert.equal(checked("()"), "1:1 a list must start with an operator");
  assert.equal(checked("(1 2 3)"), "1:1 a list must start with an operator");
  assert.equal(checked("((+ 1 2) 3 4)"), "1:1 a list must start with an operator");
});

test("an error in a branch nothing evaluates is still found", () => {
  assert.equal(checked("(+ 1 (foo))"), "1:7 unknown name foo");
});

test("booleans, comparisons and if", () => {
  assert.equal(checked("(if (< 1 2) #true #false)"), "ok");
  assert.equal(checked("(== #true 1)"), "ok");
  assert.equal(checked("#true"), "ok");
});

test("an if with other than three parts, even in a branch never taken (D13, D28)", () => {
  assert.equal(checked("(if #true 1)"), "1:1 if takes 3 arguments, not 2");
  assert.equal(checked("(if)"), "1:1 if takes 3 arguments, not 0");
  assert.equal(checked("(if #true 1 2 3)"), "1:1 if takes 3 arguments, not 4");
  assert.equal(checked("(if #false (+ 1 2 3) 0)"), "1:12 + takes 2 arguments, not 3");
  assert.equal(checked("(if #true 0 (if 1 2))"), "1:13 if takes 3 arguments, not 2");
});

test("if on its own is an unknown name, and #true is no operator", () => {
  assert.equal(checked("(+ 1 if)"), "1:6 unknown name if");
  assert.equal(checked("(#true 1 2)"), "1:1 a list must start with an operator");
  assert.equal(checked("#maybe"), "1:1 unknown name #maybe");
});

test("the bit operations take two arguments", () => {
  assert.equal(checked("(bit/and 1 2)"), "ok");
  assert.equal(checked("(bit/not 1)"), "1:2 unknown name bit/not");
  assert.equal(checked("(bit/shl 1)"), "1:1 bit/shl takes 2 arguments, not 1");
});

test("** takes two arguments", () => {
  assert.equal(checked("(** 2 3)"), "ok");
  assert.equal(checked("(** 2)"), "1:1 ** takes 2 arguments, not 1");
});

test("within takes two parts, checked in an untaken branch too (D24, D28)", () => {
  assert.equal(checked("(within 1 2)"), "ok");
  assert.equal(checked("(within)"), "1:1 within takes 2 arguments, not 0");
  assert.equal(checked("(within 5)"), "1:1 within takes 2 arguments, not 1");
  assert.equal(checked("(within 1 2 3)"), "1:1 within takes 2 arguments, not 3");
  assert.equal(checked("(if #false (within 1) 0)"), "1:12 within takes 2 arguments, not 1");
  assert.equal(checked("(+ 1 within)"), "1:6 unknown name within");
});

test("the string operators' counts (D33)", async () => {
  const { run } = await import("./helper.ts");
  assert.equal(run('(str/len "a" "b")'), "error 1:1 str/len takes 1 argument, not 2");
  assert.equal(run("(str/char)"), "error 1:1 str/char takes 1 argument, not 0");
  assert.equal(run('(str/code "a" "b")'), "error 1:1 str/code takes 1 argument, not 2");
  assert.equal(run('(str/at "a")'), "error 1:1 str/at takes 2 arguments, not 1");
  assert.equal(run('(str/cat "a" "b" "c")'), "error 1:1 str/cat takes 2 arguments, not 3");
  assert.equal(run('(if #false (str/len) 1)'), "error 1:12 str/len takes 1 argument, not 0");
});
