import { test } from "node:test";
import assert from "node:assert/strict";
import { run, err, fault } from "./helpers.ts";

test("booleans print as written", () => {
  assert.equal(run("#true"), "#true");
  assert.equal(run("#false"), "#false");
});

test("orderings on integers, == and != on any two values (D12)", () => {
  assert.equal(run("(< 1 2)"), "#true");
  assert.equal(run("(<= 2 2)"), "#true");
  assert.equal(run("(> 1 2)"), "#false");
  assert.equal(run("(>= 1 2)"), "#false");
  assert.equal(run("(== #true #true)"), "#true");
  assert.equal(run("(== 1 #true)"), "#false");
  assert.equal(run("(!= 1 #true)"), "#true");
  assert.equal(run("(== (< 1 2) (> 2 1))"), "#true");
  assert.equal(run("(== 4611686018427387903 4611686018427387903)"), "#true");
});

test("an ordering or arithmetic on a boolean faults (D11, D12)", () => {
  assert.equal(fault("(< #true 1)"), "not an integer");
  assert.equal(fault("(>= 1 #false)"), "not an integer");
  assert.equal(fault("(+ 1 #true)"), "not an integer");
  assert.equal(fault("(* #true #false)"), "not an integer");
});

test("if evaluates only the taken branch (D13)", () => {
  assert.equal(run("(if #true 1 (/ 1 0))"), "1");
  assert.equal(run("(if (< 2 1) (/ 1 0) 7)"), "7");
});

test("the test must be a boolean (D13)", () => {
  assert.equal(fault("(if 0 1 2)"), "not a boolean");
  assert.equal(fault("(if (- 1 1) 1 2)"), "not a boolean");
});

test("if with other than three parts is an error before running, taken or not (D13, D28)", () => {
  assert.equal(err("(if #true 1)"), "1:1: if takes 3 arguments, not 2");
  assert.equal(err("(if)"), "1:1: if takes 3 arguments, not 0");
  assert.equal(err("(if #true 1 2 3)"), "1:1: if takes 3 arguments, not 4");
  assert.equal(err("(if #false (if 1 2) 0)"), "1:12: if takes 3 arguments, not 2");
  assert.equal(err("(if #true 0 (/ 1 0) (+ 1 2 3))"), "1:1: if takes 3 arguments, not 4");
});

test("if and the boolean names are not values on their own", () => {
  assert.equal(err("if"), "1:1: unknown name: if");
  assert.equal(err("(+ 1 #maybe)"), "1:6: unknown name: #maybe");
  assert.equal(err("(#true 1 2)"), "1:2: unknown name: #true");
});
