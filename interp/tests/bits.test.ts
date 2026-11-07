import { test } from "node:test";
import assert from "node:assert/strict";
import { run, err, fault } from "./helpers.ts";

test("and, or, xor on the sign-extended values (D15)", () => {
  assert.equal(run("(bit/and -1 7)"), "7");
  assert.equal(run("(bit/or -8 1)"), "-7");
  assert.equal(run("(bit/xor -1 0)"), "-1");
  assert.equal(run("(bit/xor -4611686018427387904 4611686018427387903)"), "-1");
});

test("shl is times 2^n, faulting overflow past the range (D16)", () => {
  assert.equal(fault("(bit/shl 1 62)"), "overflow");
  assert.equal(run("(bit/shl -1 62)"), "-4611686018427387904");
  assert.equal(run("(bit/shl 3 4)"), "48");
  assert.equal(run("(bit/shl 0 62)"), "0");
  assert.equal(fault("(bit/shl 2 62)"), "overflow");
});

test("shr rounds toward negative infinity (D16)", () => {
  assert.equal(run("(bit/shr -7 1)"), "-4");
  assert.equal(run("(/ -7 2)"), "-3");
  assert.equal(run("(bit/shr 7 1)"), "3");
  assert.equal(run("(bit/shr -1 62)"), "-1");
  assert.equal(run("(bit/shr 4611686018427387903 62)"), "0");
});

test("a count outside 0 to 62 faults bad shift (D16)", () => {
  for (const op of ["bit/shl", "bit/shr"])
    for (const n of ["63", "-1", "4611686018427387903", "-4611686018427387904"])
      assert.equal(fault(`(${op} 1 ${n})`), "bad shift");
  assert.equal(run("(bit/shr 8 0)"), "8");
});

test("a boolean faults not an integer, and wins over a bad count", () => {
  assert.equal(fault("(bit/and #true 1)"), "not an integer");
  assert.equal(fault("(bit/shl 1 #false)"), "not an integer");
  assert.equal(fault("(bit/shl #true 99)"), "not an integer");
  assert.equal(fault("(bit/shr 7 -1)"), "bad shift");
});

test("arity is 2 (D3)", () => {
  assert.equal(err("(bit/and 1)"), "1:1: bit/and takes 2 arguments, not 1");
  assert.equal(err("(bit/not 1)"), "1:2: unknown name: bit/not");
});
