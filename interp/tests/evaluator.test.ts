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
