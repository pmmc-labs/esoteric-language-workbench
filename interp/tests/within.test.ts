import { test } from "node:test";
import assert from "node:assert/strict";
import { run, err, fault } from "./helpers.ts";

test("n operations in a budget of n; the next is refused (D22)", () => {
  assert.equal(run("(within 3 (+ (* 2 3) (- 10 4)))"), "12");
  assert.equal(fault("(within 2 (+ (* 2 3) (- 10 4)))"), "budget spent");
  assert.equal(run("(within 0 42)"), "42");
});

test("the charge is after the operands and before the checks (D22)", () => {
  assert.equal(fault("(within 1 (+ (/ 1 0) 2))"), "division by zero");
  assert.equal(fault("(within 0 (/ 1 0))"), "budget spent");
  assert.equal(fault("(within 0 (== 1 1))"), "budget spent");
  assert.equal(fault("(within 0 (+ #true 1))"), "budget spent");
});

test("if, within and literals are free, and the branch not taken costs nothing (D21)", () => {
  assert.equal(run("(within 0 (if #true (within 0 7) (/ 1 0)))"), "7");
  assert.equal(run("(within 2 (if (< 1 2) (+ 40 2) (+ (+ 1 1) (+ 1 1))))"), "42");
});

test("every budget in force applies; the inner's unused part is dropped (D23)", () => {
  assert.equal(fault("(within 1 (within 5 (+ (+ 1 2) 3)))"), "budget spent");
  assert.equal(fault("(within 5 (within 1 (+ (+ 1 2) 3)))"), "budget spent");
  assert.equal(run("(within 3 (+ (within 5 (+ (+ 1 2) 3)) 4))"), "10");
  assert.equal(fault("(within 2 (+ (within 5 (+ (+ 1 2) 3)) 4))"), "budget spent");
});

test("a budget after an inner one has ended is the outer's again (D23)", () => {
  // Five operations in all: the inner's one, the two additions and their sum, the outer's own.
  assert.equal(run("(within 5 (+ (within 1 (+ 1 1)) (+ (+ 1 1) (+ 1 1))))"), "6");
  assert.equal(fault("(within 4 (+ (within 1 (+ 1 1)) (+ (+ 1 1) (+ 1 1))))"), "budget spent");
});

test("outside every within nothing is counted (D23)", () => {
  assert.equal(run("(+ (within 1 (+ 1 1)) (+ (+ 1 1) (+ 1 1)))"), "6");
});

test("the budget is any expression, evaluated outside its own budget (D24)", () => {
  assert.equal(run("(within 2 (within (+ 1 1) (* 3 4)))"), "12");
  assert.equal(fault("(within 1 (within (+ 1 1) (* 3 4)))"), "budget spent");
});

test("the budget must be an integer, then not negative, before the body runs (D24)", () => {
  assert.equal(fault("(within #true 1)"), "not an integer");
  assert.equal(fault("(within -1 (/ 1 0))"), "bad budget");
  assert.equal(fault("(within (< 1 2) (/ 1 0))"), "not an integer");
});

test("the budget may be any integer up to the largest, and the body is of any type", () => {
  assert.equal(run("(within 4611686018427387903 (+ 1 2))"), "3");
  assert.equal(run("(within 1 (< 1 2))"), "#true");
});

test("the first fault in left-to-right order is the one reported (D25)", () => {
  assert.equal(fault("(+ (/ 1 0) (+ #true 1))"), "division by zero");
  assert.equal(fault("(within 1 (+ (* 2 3) (/ 1 0)))"), "budget spent");
});

test("within takes two parts, checked before running (D24, D28)", () => {
  assert.equal(err("(within)"), "1:1: within takes 2 arguments, not 0");
  assert.equal(err("(within 5)"), "1:1: within takes 2 arguments, not 1");
  assert.equal(err("(within 1 2 3)"), "1:1: within takes 2 arguments, not 3");
  assert.equal(err("(if #false (within 1) 0)"), "1:12: within takes 2 arguments, not 1");
  assert.equal(err("within"), "1:1: unknown name: within");
});
