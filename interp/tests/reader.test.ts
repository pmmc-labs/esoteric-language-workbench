import { test } from "node:test";
import assert from "node:assert/strict";
import { read, MAX_DEPTH } from "../src/reader.ts";
import { CheckError } from "../src/errors.ts";

const err = (src: string) => {
  try { read(src); } catch (e) {
    assert.ok(e instanceof CheckError);
    return `${e.line}:${e.col} ${e.message}`;
  }
  assert.fail("no error");
};

test("an integer, with its position", () => {
  assert.deepEqual(read("  42"), { t: "int", v: 42n, line: 1, col: 3 });
  assert.deepEqual(read("-7"), { t: "int", v: -7n, line: 1, col: 1 });
});

test("the range's edges are accepted", () => {
  assert.equal((read("4611686018427387903") as any).v, 4611686018427387903n);
  assert.equal((read("-4611686018427387904") as any).v, -4611686018427387904n);
});

test("a literal past the range is an error before running", () => {
  assert.equal(err("4611686018427387904"), "1:1 integer 4611686018427387904 is out of range (63 bits)");
  assert.equal(err("\n  -4611686018427387905"), "2:3 integer -4611686018427387905 is out of range (63 bits)");
});

test("lists and symbols, each with line and column", () => {
  const f = read("(+ 1\n   (* 2 3))");
  assert.equal(f.t, "list");
  if (f.t !== "list") return;
  assert.deepEqual([f.line, f.col], [1, 1]);
  assert.deepEqual(f.items[0], { t: "sym", name: "+", line: 1, col: 2 });
  const inner = f.items[2];
  assert.deepEqual([inner.line, inner.col], [2, 4]);
});

test("a symbol that starts like a number is a symbol", () => {
  assert.equal(read("+5").t, "sym");
  assert.equal(read("1a").t, "sym");
  assert.equal(read("-").t, "sym");
});

test("comments run to the end of the line", () => {
  assert.equal((read("; one\n42 ; two\n; three") as any).v, 42n);
  assert.equal(read("(+ 1 ;)\n 2)").t, "list");
});

test("errors: nothing, two programs, unbalanced", () => {
  assert.equal(err(""), "1:1 expected an expression");
  assert.equal(err("; only a comment\n"), "2:1 expected an expression");
  assert.equal(err("1 2"), "1:3 unexpected form after the program");
  assert.equal(err("(+ 1 2) (+ 3 4)"), "1:9 unexpected form after the program");
  assert.equal(err("(+ 1 2))"), "1:8 unmatched )");
  assert.equal(err("(+ 1\n  (* 2 3)"), "1:1 unclosed (");
});

test("nesting is limited, and reads deep without the host's stack", () => {
  const ok = "(".repeat(MAX_DEPTH) + ")".repeat(MAX_DEPTH);
  assert.equal(read(ok).t, "list");
  assert.equal(err("(".repeat(MAX_DEPTH + 1) + ")".repeat(MAX_DEPTH + 1)),
    `1:${MAX_DEPTH + 1} nested too deeply (limit ${MAX_DEPTH})`);
});
