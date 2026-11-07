import { test } from "node:test";
import assert from "node:assert/strict";
import { run } from "./helper.ts";

test("arithmetic, nested (D3, D5)", () => {
  assert.equal(run("(+ (* 6 7) (- 10 (/ 7 2)))"), "49");
  assert.equal(run("(/ -7 2)"), "-3");
  assert.equal(run("(% -7 2)"), "-1");
  assert.equal(run("(% 7 -2)"), "1");
  assert.equal(run("(/ 7 -2)"), "-3");
});

test("overflow at both edges, and in a quotient (D4)", () => {
  assert.equal(run("(+ 4611686018427387903 1)"), "fault: overflow");
  assert.equal(run("(- -4611686018427387904 1)"), "fault: overflow");
  assert.equal(run("(* 3037000500 3037000500)"), "fault: overflow");
  assert.equal(run("(/ -4611686018427387904 -1)"), "fault: overflow");
  assert.equal(run("(- 0 -4611686018427387904)"), "fault: overflow");
  assert.equal(run("(+ 4611686018427387903 -4611686018427387904)"), "-1");
  assert.equal(run("(% -4611686018427387904 -1)"), "0");
});

test("division by zero (D6)", () => {
  assert.equal(run("(/ 1 0)"), "fault: division by zero");
  assert.equal(run("(% 1 0)"), "fault: division by zero");
});

test("a deep right-nested program evaluates", () => {
  const n = 900;
  assert.equal(run("(+ 1 ".repeat(n) + "0" + ")".repeat(n)), String(n));
});

test("booleans print as written; comparisons give booleans (D11, D12)", () => {
  assert.equal(run("#true"), "#true");
  assert.equal(run("(< 1 2)"), "#true");
  assert.equal(run("(>= 1 2)"), "#false");
  assert.equal(run("(<= -4611686018427387904 4611686018427387903)"), "#true");
});

test("== and != on any two values, never coercing (D12)", () => {
  assert.equal(run("(== 1 #true)"), "#false");
  assert.equal(run("(== 0 #false)"), "#false");
  assert.equal(run("(!= 0 #false)"), "#true");
  assert.equal(run("(== #true #true)"), "#true");
  assert.equal(run("(== (+ 1 1) 2)"), "#true");
  assert.equal(run("(!= 1 1)"), "#false");
});

test("arithmetic and orderings fault on a boolean (D11)", () => {
  assert.equal(run("(+ 1 #true)"), "fault: not an integer");
  assert.equal(run("(< #false 1)"), "fault: not an integer");
  assert.equal(run("(+ 1 (if #true #false 0))"), "fault: not an integer");
});

test("if: a boolean test, one branch evaluated (D13)", () => {
  assert.equal(run("(if #true 1 (/ 1 0))"), "1");
  assert.equal(run("(if #false (/ 1 0) 2)"), "2");
  assert.equal(run("(if (- 1 1) 1 2)"), "fault: not a boolean");
  assert.equal(run("(if #true #false 3)"), "#false");
});

test("evaluation is left to right (D25)", () => {
  assert.equal(run("(+ (/ 1 0) (+ #true 1))"), "fault: division by zero");
  assert.equal(run("(+ (+ #true 1) (/ 1 0))"), "fault: not an integer");
});
