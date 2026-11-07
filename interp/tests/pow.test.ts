import { test } from "node:test";
import assert from "node:assert/strict";
import { run, fault } from "./helpers.ts";

test("powers (D18)", () => {
  assert.equal(run("(** 2 10)"), "1024");
  assert.equal(run("(** -3 3)"), "-27");
  assert.equal(run("(** -2 61)"), "-2305843009213693952");
});

test("a ** 0 is 1 for every a, 0 ** 0 too (D19)", () => {
  for (const a of ["0", "1", "-1", "7", "-4611686018427387904"]) assert.equal(run(`(** ${a} 0)`), "1");
});

test("a negative exponent faults bad exponent, even where the answer fits (D19)", () => {
  assert.equal(fault("(** 2 -1)"), "bad exponent");
  assert.equal(fault("(** 1 -1)"), "bad exponent");
  assert.equal(fault("(** 0 -1)"), "bad exponent");
});

test("a result past the range faults overflow, however large the exponent (D4, D19)", () => {
  assert.equal(fault("(** 2 62)"), "overflow");
  assert.equal(run("(** 2 61)"), "2305843009213693952");
  assert.equal(run("(** -2 62)".replace("-2 62", "-2 61")), "-2305843009213693952");
  assert.equal(fault("(** 2 4611686018427387903)"), "overflow");
  assert.equal(fault("(** -2 4611686018427387903)"), "overflow");
  assert.equal(fault("(** 4611686018427387903 2)"), "overflow");
});

test("0, 1 and -1 to a huge exponent are quick and exact", () => {
  assert.equal(run("(** 1 4611686018427387903)"), "1");
  assert.equal(run("(** 0 4611686018427387903)"), "0");
  assert.equal(run("(** -1 4611686018427387903)"), "-1");
  assert.equal(run("(** -1 4611686018427387902)"), "1");
});

test("a boolean faults not an integer (D19)", () => {
  assert.equal(fault("(** #true 2)"), "not an integer");
  assert.equal(fault("(** 2 #false)"), "not an integer");
});
