import { test } from "node:test";
import assert from "node:assert/strict";
import { run, err } from "./helpers.ts";

test("one literal", () => {
  assert.equal(run("42"), "42");
  assert.equal(run("-4611686018427387904"), "-4611686018427387904");
});

test("a program is one expression", () => {
  assert.equal(err(""), "1:1: empty program");
  assert.equal(err("; only a comment\n"), "1:1: empty program");
  assert.equal(err("1\n 2"), "2:2: a program is one expression");
});

test("an unknown name", () => {
  assert.equal(err("foo"), "1:1: unknown name: foo");
});
