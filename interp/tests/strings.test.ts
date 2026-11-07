import { test } from "node:test";
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { writeFileSync, mkdirSync } from "node:fs";
import { read } from "../src/reader.ts";
import { check } from "../src/checker.ts";
import { CheckError } from "../src/errors.ts";
import { run } from "./helper.ts";

// The error before running as `L:C message`, or "ok" (D28).
const err = (src: string) => {
  try { check(read(src)); return "ok"; } catch (e) {
    assert.ok(e instanceof CheckError, String(e));
    return `${e.line}:${e.col} ${e.message}`;
  }
};

test("escapes in a literal (D31)", () => {
  const f = read('"a\\"b\\\\c\\nd\\te\\u{41}\\u{1F600}"');
  assert.equal(f.t, "str");
  if (f.t === "str") assert.equal(f.v, 'a"b\\c\nd\teA\u{1F600}');
});

test("a raw tab, carriage return, ; and ( stand for themselves (D31)", () => {
  assert.equal((read('"a\tb\rc;(d"') as { v: string }).v, "a\tb\rc;(d");
});

test("\\u{X} takes one to six hex digits, leading zeros and all (D31)", () => {
  assert.equal((read('"\\u{0041}"') as { v: string }).v, "A");
  assert.equal((read('"\\u{10FFFF}"') as { v: string }).v, "\u{10FFFF}");
  assert.equal((read('"\\u{0}"') as { v: string }).v, "\u0000");
});

test("a quote ends a name or an integer (D31)", () => {
  assert.equal((read('(str/len"a")') as { items: unknown[] }).items.length, 2);
  assert.equal(err('"a""b"'), "1:4 unexpected form after the program");
});

test("the errors of a literal, each at its place (D31, D34)", () => {
  assert.equal(err('"abc'), "1:1 unclosed string");
  assert.equal(err('(str/cat "x" "abc\n  ")'), "1:18 newline in string");
  assert.equal(err('"\\q"'), "1:2 bad escape");
  assert.equal(err('"ab\\'), "1:1 unclosed string");
  assert.equal(err('"\\u41"'), "1:2 bad escape");
  assert.equal(err('"\\u{}"'), "1:2 bad escape");
  assert.equal(err('"\\u{0000041}"'), "1:2 bad escape");
  assert.equal(err('"\\u{zz}"'), "1:2 bad escape");
  assert.equal(err('"\\u{D800}"'), "1:2 bad escape");
  assert.equal(err('"\\u{DFFF}"'), "1:2 bad escape");
  assert.equal(err('"\\u{110000}"'), "1:2 bad escape");
  assert.equal(err("(str/cat \"x\" \"\\u{1F600"), "1:15 bad escape");
});

test("a column counts code points, not UTF-16 units (D31)", () => {
  // The integer is at column 14: the emoji is one column, two units.
  assert.equal(err('(str/cat "\u{1F600}" 4611686018427387904)'), "1:14 integer 4611686018427387904 is out of range (63 bits)");
});

test("a byte order mark and no-break space are characters of a name (D31)", () => {
  assert.equal(read("﻿42").t, "sym");
  assert.equal(err(" "), "1:1 unknown name  ");
  assert.equal(err("\f"), "1:1 unknown name \f");
});

test("a string is one value, and the arity of the string operators (D33)", () => {
  assert.equal(err('(str/len "a" "b")'), "1:1 str/len takes 1 argument, not 2");
  assert.equal(err('(str/cat "a")'), "1:1 str/cat takes 2 arguments, not 1");
  assert.equal(err('(str/char)'), "1:1 str/char takes 1 argument, not 0");
  assert.equal(err('(if "x" 1)'), "1:1 if takes 3 arguments, not 2");
});

test("printing: D32's escapes, and everything else as itself", () => {
  assert.equal(run('"\\u{7}\\"\\\\\\n\\t"'), '"\\u{7}\\"\\\\\\n\\t"');
  assert.equal(run('"é\u{1F600}\u0080 "'), '"é\u{1F600}\u0080 "');
  assert.equal(run('""'), '""');
});

test("equality is by code points, and across types (D12, D33)", () => {
  assert.equal(run('(== "é" "e\\u{301}")'), "#false");
  assert.equal(run('(== "\u{1F600}" "\\u{1F600}")'), "#true");
  assert.equal(run('(!= "a" 1)'), "#true");
  assert.equal(run('(== "" #false)'), "#false");
});

test("the six operators (D33)", () => {
  assert.equal(run('(str/len "a\u{1F600}e\\u{301}")'), "4");
  assert.equal(run('(str/at "a\u{1F600}b" 1)'), '"\u{1F600}"');
  assert.equal(run('(str/cat "a" "b")'), '"ab"');
  assert.equal(run('(str/lt "a" "ab")'), "#true");
  assert.equal(run('(str/lt "ab" "a")'), "#false");
  assert.equal(run('(str/lt "\\u{FFFF}" "\\u{10000}")'), "#true");
  assert.equal(run('(str/code "\\u{1F600}")'), "128512");
  assert.equal(run('(str/char 128512)'), '"\u{1F600}"');
});

test("the faults, in D33's order", () => {
  assert.equal(run('(str/at 5 #true)'), "fault: not a string");
  assert.equal(run('(str/at "ab" 7)'), "fault: bad index");
  assert.equal(run('(str/at "ab" "x")'), "fault: not an integer");
  assert.equal(run('(str/at "ab" -1)'), "fault: bad index");
  assert.equal(run('(str/code "")'), "fault: not a character");
  assert.equal(run('(str/code "ab")'), "fault: not a character");
  assert.equal(run('(str/char 55296)'), "fault: not a character");
  assert.equal(run('(str/char 1114112)'), "fault: not a character");
  assert.equal(run('(str/char #true)'), "fault: not an integer");
  assert.equal(run('(str/cat 1 "a")'), "fault: not a string");
  assert.equal(run('(str/len 1)'), "fault: not a string");
  assert.equal(run('(+ 1 "1")'), "fault: not an integer");
  assert.equal(run('(< "a" "b")'), "fault: not an integer");
  assert.equal(run('(if "x" 1 2)'), "fault: not a boolean");
});

test("a string operator is one operation for a budget (D21, D22)", () => {
  assert.equal(run('(within 1 (str/len "a"))'), "1");
  assert.equal(run('(within 0 (str/len "a"))'), "fault: budget spent");
  assert.equal(run('(within 2 (str/at "ab" 9))'), "fault: bad index");
  assert.equal(run('(within 1 (str/at "ab" 9))'), "fault: bad index");
  assert.equal(run('(within 0 (str/at "ab" 9))'), "fault: budget spent");
});

test("the driver: strict UTF-8, a byte order mark kept, UTF-8 out", () => {
  mkdirSync("build/unit", { recursive: true });
  const go = (name: string, bytes: Buffer) => {
    const path = `build/unit/${name}.lang`;
    writeFileSync(path, bytes);
    return spawnSync(process.execPath, ["bin/lang.ts", path], { encoding: "utf8" });
  };
  const bad = go("bad-utf8", Buffer.from([0x22, 0xff, 0x22]));
  assert.equal(bad.status, 2);
  assert.equal(bad.stderr, "build/unit/bad-utf8.lang:1:1: not valid UTF-8\n");
  const bom = go("bom", Buffer.from("﻿42"));
  assert.equal(bom.status, 2);
  assert.equal(bom.stderr, "build/unit/bom.lang:1:1: unknown name ﻿42\n");
  const ok = go("utf8", Buffer.from('"é"'));
  assert.equal(ok.status, 0);
  assert.deepEqual(Buffer.from(ok.stdout, "utf8"), Buffer.from('"é"\n', "utf8"));
});
