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

// The expression as an s-expression, so precedence reads off the string.
import type { Expr } from "../src/parser.ts";
const show = (e: Expr): string =>
  e.k === "int" ? e.v : e.k === "un" ? `(${e.op} ${show(e.e)})` : `(${e.op} ${show(e.l)} ${show(e.r)})`;
const sx = (src: string) => show(parse(lex("print " + src)).stmts[0].e);

test("precedence, loosest to tightest", () => {
  assert.equal(sx("1 or 2 and 3"), "(or 1 (and 2 3))");
  assert.equal(sx("1 and 2 or 3"), "(or (and 1 2) 3)");
  assert.equal(sx("not 1 and 2"), "(and (not 1) 2)");
  assert.equal(sx("not 1 = 2"), "(not (= 1 2))");
  assert.equal(sx("not not 1"), "(not (not 1))");
  assert.equal(sx("1 + 2 < 3 * 4"), "(< (+ 1 2) (* 3 4))");
  assert.equal(sx("1 + 2 * 3"), "(+ 1 (* 2 3))");
  assert.equal(sx("1 * 2 + 3"), "(+ (* 1 2) 3)");
  assert.equal(sx("-1 * 2"), "(* (- 1) 2)");
  assert.equal(sx("- -1"), "(- (- 1))");
  assert.equal(sx("2 - -3"), "(- 2 (- 3))");
  assert.equal(sx("(1 + 2) * 3"), "(* (+ 1 2) 3)");
  assert.equal(sx("1 = 2 and 3 != 4 or 5 <= 6 and 7 >= 8 and 9 > 0"),
    "(or (and (= 1 2) (!= 3 4)) (and (and (<= 5 6) (>= 7 8)) (> 9 0)))");
});

test("+ - and * / % are left to right", () => {
  assert.equal(sx("1 - 2 - 3"), "(- (- 1 2) 3)");
  assert.equal(sx("1 + 2 - 3"), "(- (+ 1 2) 3)");
  assert.equal(sx("8 / 4 / 2"), "(/ (/ 8 4) 2)");
  assert.equal(sx("8 / 4 * 2 % 3"), "(% (* (/ 8 4) 2) 3)");
  assert.equal(sx("1 and 2 and 3"), "(and (and 1 2) 3)");
});

test("operators carry their own position", () => {
  const e = parse(lex("print 1 +\n  2 * 3")).stmts[0].e;
  assert.ok(e.k === "bin" && e.line === 1 && e.col === 9);
  assert.ok(e.k === "bin" && e.r.k === "bin" && e.r.line === 2 && e.r.col === 5);
});

test("expression errors", () => {
  assert.equal(err("print 1 <").msg, "expected expression, found end of file");
  assert.equal(err("print 1 + * 2").msg, "expected expression, found '*'");
  assert.equal(err("print not").msg, "expected expression, found end of file");
  assert.equal(err("print 1 + not 2").msg, "expected expression, found 'not'");
  assert.deepEqual(err("print (1 + 2"), { line: 1, col: 13, msg: "expected ')', found end of file" });
  assert.equal(err("print ()").msg, "expected expression, found ')'");
  assert.equal(err("print 1 )").msg, "expected statement, found ')'");
  // At most one comparison per level (LANGUAGE.md): the second is left over.
  assert.deepEqual(err("print 1 < 2 < 3"), { line: 1, col: 13, msg: "expected statement, found '<'" });
  assert.equal(err("print 1 = 2 = 3").msg, "expected statement, found '='");
  assert.equal(err("print 1 < 2 != 3").msg, "expected statement, found '!='");
});

test("write is a statement", () => {
  assert.deepEqual(parse(lex("write 1 print 2")).stmts.map((s) => s.k), ["write", "print"]);
});

test("codegen: operands in source order, right side of and/or under an if", () => {
  const c = codegen(parse(lex("print 1 / 0 + 2 * 3")));
  assert.ok(c.indexOf("INT64_C(1)") < c.indexOf("INT64_C(0)"));
  assert.ok(c.indexOf("strata_div") < c.indexOf("INT64_C(2)"));
  const l = codegen(parse(lex("print 0 and 1 / 0")));
  assert.ok(l.indexOf("if (strata_truth(") < l.indexOf("strata_div"));
  assert.ok(codegen(parse(lex("print 1 or 2"))).includes("if (!strata_truth("));
});
