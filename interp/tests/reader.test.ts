import { test } from "node:test";
import assert from "node:assert/strict";
import { read } from "../src/reader.ts";
import { CompileError } from "../src/errors.ts";

const err = (src: string) => {
  try { read(src); } catch (e) { return e as CompileError; }
  assert.fail("no error");
};

test("an integer, with its position", () => {
  assert.deepEqual(read("  42"), [{ kind: "int", value: 42n, line: 1, col: 3 }]);
});

test("a list of forms, and positions across lines", () => {
  const [f] = read("(+ 1\n  (- 2 3))");
  assert.equal(f.kind, "list");
  if (f.kind !== "list") return;
  assert.deepEqual([f.line, f.col], [1, 1]);
  assert.deepEqual(f.items.map((x) => [x.kind, x.line, x.col]), [["sym", 1, 2], ["int", 1, 4], ["list", 2, 3]]);
});

test("negative integers, and - alone is a symbol", () => {
  const [a, b] = read("-5 -");
  assert.equal(a.kind === "int" && a.value, -5n);
  assert.equal(b.kind, "sym");
});

test("comments run to the end of the line", () => {
  assert.equal(read("; hi\n7 ; there\n").length, 1);
});

test("the integers' limits are 63 bits", () => {
  assert.equal((read("4611686018427387903")[0] as { value: bigint }).value, 4611686018427387903n);
  assert.equal((read("-4611686018427387904")[0] as { value: bigint }).value, -4611686018427387904n);
});

test("a literal past the range is an error at its position", () => {
  for (const [src, col] of [["4611686018427387904", 1], ["(+ 1 -4611686018427387905)", 6]] as const) {
    const e = err(src);
    assert.match(e.message, /out of range/);
    assert.deepEqual([e.line, e.col], [1, col]);
  }
});

test("unbalanced brackets", () => {
  const a = err("(+ 1 2");
  assert.deepEqual([a.message, a.line, a.col], ["unclosed (", 1, 1]);
  const b = err("1\n )");
  assert.deepEqual([b.message, b.line, b.col], ["unexpected )", 2, 2]);
});

test("a deep program doesn't overflow the stack", () => {
  const n = 100000;
  assert.equal(read("(".repeat(n) + ")".repeat(n)).length, 1);
});
