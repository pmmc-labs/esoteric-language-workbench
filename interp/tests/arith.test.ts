import { test } from "node:test";
import assert from "node:assert/strict";
import { run, err, fault } from "./helpers.ts";

test("the five operators, nested", () => {
  assert.equal(run("(+ (* 6 7) (- 10 (/ 7 2)))"), "49");
});

test("division truncates toward zero and % takes the dividend's sign (D5)", () => {
  assert.equal(run("(/ -7 2)"), "-3");
  assert.equal(run("(% -7 2)"), "-1");
  assert.equal(run("(/ 7 -2)"), "-3");
  assert.equal(run("(% 7 -2)"), "1");
});

test("a result past 63 bits faults overflow (D4)", () => {
  assert.equal(fault("(+ 4611686018427387903 1)"), "overflow");
  assert.equal(fault("(- -4611686018427387904 1)"), "overflow");
  assert.equal(fault("(* 4611686018427387903 2)"), "overflow");
  assert.equal(fault("(/ -4611686018427387904 -1)"), "overflow");
  assert.equal(run("(% -4611686018427387904 -1)"), "0");
});

test("division by zero faults (D5)", () => {
  assert.equal(fault("(/ 1 0)"), "division by zero");
  assert.equal(fault("(% 1 0)"), "division by zero");
});

test("the left operand's fault is the one reported (D25)", () => {
  assert.equal(fault("(+ (/ 1 0) (+ (* 4611686018427387903 2) 1))"), "division by zero");
});

test("operators with other than two operands are errors before running (D3, D7)", () => {
  assert.equal(err("(+ 1 2 3)"), "1:1: + takes 2 arguments, not 3");
  assert.equal(err("(- 1)"), "1:1: - takes 2 arguments, not 1");
  assert.equal(err("(+)"), "1:1: + takes 2 arguments, not 0");
  assert.equal(err("(+ 1\n  (* 2))"), "2:3: * takes 2 arguments, not 1");
});

test("an unknown name, a head that isn't an operator", () => {
  assert.equal(err("(foo 1 2)"), "1:2: unknown name: foo");
  assert.equal(err("(+ 1 x)"), "1:6: unknown name: x");
  assert.equal(err("(toString 1 2)"), "1:2: unknown name: toString");
  assert.equal(err("(1 2 3)"), "1:2: not an operator");
  assert.equal(err("((+ 1 2) 3)"), "1:2: not an operator");
  assert.equal(err("()"), "1:1: empty list");
});

test("an error before running wins over an earlier fault", () => {
  assert.equal(err("(+ (/ 1 0) (+ 1 2 3))"), "1:12: + takes 2 arguments, not 3");
});

test("the first error in reading order is the one reported", () => {
  assert.equal(err("(+ (foo 1) (+ 1))"), "1:5: unknown name: foo");
});
