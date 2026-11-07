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

const str = (src: string) => (read(src) as { v: string }).v;

test("a string literal, its escapes and its position (D31)", () => {
  assert.deepEqual(read(' "ab"'), { t: "str", v: "ab", line: 1, col: 2 });
  assert.equal(str(String.raw`"\"\\\n\t"`), '"\\\n\t');
  assert.equal(str(String.raw`"\u{41}\u{1F600}\u{10FFFF}\u{000041}\u{e9}\u{E9}"`), "A😀\u{10FFFF}Aéé");
  assert.equal(str('"a\tb\rc"'), "a\tb\rc");
  assert.equal(str('"é\u{FEFF}\u{A0}"'), "é\u{FEFF}\u{A0}");
});

test("a string literal's errors are before running (D31)", () => {
  assert.equal(err(' "abc'), "1:2 unclosed string");
  assert.equal(err('\n"abc\ndef"'), "2:5 newline in a string (write \\n)");
  assert.equal(err(String.raw`"a\q"`), "1:3 bad escape \\q");
  assert.equal(err(String.raw`"a\"`), "1:1 unclosed string");
  assert.equal(err('"\\'), "1:1 unclosed string");
  assert.equal(err(String.raw`"\u41"`), "1:2 bad escape \\u: expected {");
  assert.equal(err(String.raw`"\u{}"`), "1:2 empty \\u{}");
  assert.equal(err(String.raw`"\u{1234567}"`), "1:2 \\u{...} longer than six digits");
  assert.equal(err(String.raw`"\u{12G}"`), "1:2 \\u{12G} is not hex");
  assert.equal(err(String.raw`"\u{D800}"`), "1:2 \\u{D800} is a surrogate");
  assert.equal(err(String.raw`"\u{dFFF}"`), "1:2 \\u{dFFF} is a surrogate");
  assert.equal(err(String.raw`"\u{110000}"`), "1:2 \\u{110000} is past 10FFFF");
  assert.equal(err(String.raw`"\u{41"`), "1:2 unclosed \\u{");
  assert.equal(str(String.raw`"\u{D7FF}\u{E000}"`), "\u{D7FF}\u{E000}");
});

test("a column counts code points (D31)", () => {
  const f = read('(+ "😀😀" 1)') as any;
  assert.deepEqual([f.items[1].col, f.items[2].col], [4, 9]);
  const g = read('"😀"\n') as any;
  assert.equal(g.col, 1);
  assert.equal(err('"😀" 😀'), "1:5 unexpected form after the program");
  assert.equal(err('"😀"x"'), "1:4 unexpected form after the program");
});

test("a quote ends a name and an integer as a bracket does (D31)", () => {
  const f = read('(str/len"a")') as any;
  assert.deepEqual([f.items[0].name, f.items[1].v], ["str/len", "a"]);
  assert.equal(err('"a""b"'), "1:4 unexpected form after the program");
  const g = read('(+ 1"a")') as any;
  assert.deepEqual([g.items[1].v, g.items[2].v], [1n, "a"]);
});

test("white space is four characters and no more (D31)", () => {
  assert.equal(read("\u{A0}x").t, "sym");
  assert.equal((read("\u{A0}x") as any).name, "\u{A0}x");
  assert.equal(err("\u{FEFF}(+ 1 2)"), "1:2 unexpected form after the program");
});
