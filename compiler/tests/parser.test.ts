import { test } from "node:test";
import assert from "node:assert/strict";
import { lex } from "../src/lexer.ts";
import { parse } from "../src/parser.ts";
import { codegen } from "../src/codegen.ts";

const err = (src: string) => {
  try { parse(lex(src)); } catch (e) { return e as { line: number; col: number; msg: string }; }
  assert.fail("expected a compile error");
};

test("print INTEGER, any number of them", () => {
  assert.equal(parse(lex("")).stmts.length, 0);
  const p = parse(lex("print 1 print 2\nprint 3"));
  assert.deepEqual(p.stmts.map((s) => [s.e.v, s.line, s.col]), [["1", 1, 1], ["2", 1, 9], ["3", 2, 1]]);
});

test("parse errors", () => {
  assert.deepEqual(err("print"), { line: 1, col: 6, msg: "expected expression, found end of file" });
  assert.equal(err("print print").msg, "expected expression, found 'print'");
  assert.equal(err("print x").msg, "expected expression, found 'x'");
  assert.equal(err('print "s"').msg, "expected expression, found '\"s\"'");
  assert.deepEqual(err("5"), { line: 1, col: 1, msg: "expected statement, found '5'" });
  assert.equal(err("let x = 1").msg, "expected statement, found 'let'");
});

test("codegen: one temporary per literal, in source order", () => {
  const c = codegen(parse(lex("print 7\nprint 8")));
  assert.ok(c.indexOf("INT64_C(7)") < c.indexOf("INT64_C(8)"));
  assert.ok(c.includes("strata_print(t1, 1, 1);") && c.includes("strata_print(t2, 2, 1);"));
});
