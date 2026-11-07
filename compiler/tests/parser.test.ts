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
  assert.deepEqual(p.stmts.map((s) => [(s.e as { v: string }).v, s.line, s.col]), [["1", 1, 1], ["2", 1, 9], ["3", 2, 1]]);
});

test("parse errors", () => {
  assert.deepEqual(err("print"), { line: 1, col: 6, msg: "expected expression, found end of file" });
  assert.equal(err("print print").msg, "expected expression, found 'print'");
  assert.equal(err("print )").msg, "expected expression, found ')'");
  assert.equal(err('print "s"').msg, "expected expression, found '\"s\"'");
  assert.deepEqual(err("5"), { line: 1, col: 1, msg: "expected statement, found '5'" });
  assert.equal(err("let x = 1 )").msg, "expected statement, found ')'");
  assert.equal(err("let 1").msg, "expected name, found '1'");
  assert.equal(err("let x 1").msg, "expected '=', found '1'");
  assert.equal(err("x 1").msg, "expected '<-', found '1'");
  assert.equal(err("print [1, 2").msg, "expected ']', found end of file");
});

test("codegen: one temporary per literal, in source order", () => {
  const c = codegen(parse(lex("print 7\nprint 8")));
  assert.ok(c.indexOf("INT64_C(7)") < c.indexOf("INT64_C(8)"));
  assert.ok(c.includes("strata_print(t1, 1, 1);") && c.includes("strata_print(t2, 2, 1);"));
});

// The expression as an s-expression, so precedence reads off the string.
import type { Expr, Stmt } from "../src/parser.ts";
const show = (e: Expr): string =>
  e.k === "int" ? e.v
  : e.k === "name" ? e.name
  : e.k === "list" ? `[${e.elems.map(show).join(" ")}]`
  : e.k === "at" ? `(@ ${show(e.e)} ${show(e.i)})`
  : e.k === "un" ? `(${e.op} ${show(e.e)})`
  : `(${e.op} ${show(e.l)} ${show(e.r)})`;
const sx = (src: string) => show((parse(lex("print " + src)).stmts[0] as { e: Expr }).e);

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

test("@ and #: postfix binds tighter than prefix; @ chains left; k is a primary", () => {
  assert.equal(sx("x@1"), "(@ x 1)");
  assert.equal(sx("x@1@2"), "(@ (@ x 1) 2)");
  assert.equal(sx("#x@1"), "(# (@ x 1))");
  assert.equal(sx("-x@1"), "(- (@ x 1))");
  assert.equal(sx("x@1 + 2"), "(+ (@ x 1) 2)");
  assert.equal(sx("x@(i + 1)"), "(@ x (+ i 1))");
  assert.equal(sx("x@y@z"), "(@ (@ x y) z)");
  assert.equal(sx("[1, 2]@1"), "(@ [1 2] 1)");
  assert.equal(sx("##x"), "(# (# x))");
  assert.equal(sx("#x + 1"), "(+ (# x) 1)");
  assert.equal(err("print x@-1").msg, "expected expression, found '-'");
  assert.equal(err("print x@").msg, "expected expression, found end of file");
});

test("history literals, let and write", () => {
  assert.equal(sx("[]"), "[]");
  assert.equal(sx("[1, x + 1, [2]]"), "[1 (+ x 1) [2]]");
  const p = parse(lex("let a = 1\n a <- 2"));
  assert.deepEqual(p.stmts.map((s) => [s.k, s.line, s.col]), [["let", 1, 5], ["set", 2, 4]]);
});

test("codegen: @ evaluates its base before its index (D25)", () => {
  const c = codegen(parse(lex("print x@(1 / 2)".replace("x", "[7]"))));
  assert.ok(c.indexOf("INT64_C(7)") < c.indexOf("INT64_C(1)"));
  assert.ok(c.indexOf("INT64_C(1)") < c.indexOf("strata_div"));
  assert.ok(c.indexOf("strata_div") < c.indexOf("strata_at"));
});

// A statement's shape: `(if COND THEN ELSE)` with blocks as [...], `-` for
// no else; `(while COND BODY)`; other statements by their keyword (D38).
const shape = (s: Stmt): string =>
  s.k === "if" ? `(if ${show(s.cond)} [${s.then.map(shape).join(" ")}] ${s.els ? `[${s.els.map(shape).join(" ")}]` : "-"})`
  : s.k === "while" ? `(while ${show(s.cond)} [${s.body.map(shape).join(" ")}])`
  : s.k;
const shp = (src: string) => parse(lex(src)).stmts.map(shape).join(" ");

test("if, else if, else and while: blocks hold statements, else if nests", () => {
  assert.equal(shp("if 1 { print 2 } else if 3 { print 4 } else { print 5 }"),
    "(if 1 [print] [(if 3 [print] [print])])");
  assert.equal(shp("if 1 { print 2 } else if 3 { print 4 }"), "(if 1 [print] [(if 3 [print] -)])");
  assert.equal(shp("while 0 {}"), "(while 0 [])");
  assert.equal(shp("if 1 {} else {}"), "(if 1 [] [])");
  assert.equal(shp("while x@1 { if 2 { let y = 3 } write y }"), "(while (@ x 1) [(if 2 [let] -) write])");
  assert.equal(shp("print 1\nwhile 1 {\n}\nwrite 2"), "print (while 1 []) write");
});

test("if and while carry the keyword's position; so does an else if", () => {
  const p = parse(lex("let a = 1\n  while a {}\nif 0 {} else if 1 {}")).stmts;
  assert.deepEqual([p[1].line, p[1].col], [2, 3]);
  assert.equal(p[2].k === "if" && p[2].els && p[2].els[0].col, 14);
});

test("block and condition errors, in D33's shape", () => {
  assert.deepEqual(err("if 1 print 2"), { line: 1, col: 6, msg: "expected '{', found 'print'" });
  assert.equal(err("while 1").msg, "expected '{', found end of file");
  assert.equal(err("if 1 { print 2").msg, "expected '}', found end of file");
  assert.equal(err("if 1 { print 2 } else print 3").msg, "expected '{', found 'print'");
  assert.equal(err("if 1 { } else").msg, "expected '{', found end of file");
  assert.equal(err("if { }").msg, "expected expression, found '{'");
  assert.equal(err("}").msg, "expected statement, found '}'");
  assert.equal(err("if 1 { 5 }").msg, "expected statement, found '5'");
});

test("codegen: a while condition sits inside the loop; an else if inside the else (D38)", () => {
  const w = codegen(parse(lex("while 1 { print 2 }")));
  assert.ok(w.indexOf("for (;;) {") < w.indexOf("INT64_C(1)"));
  assert.ok(w.indexOf("INT64_C(1)") < w.indexOf("break;"));
  assert.ok(w.indexOf("break;") < w.indexOf("INT64_C(2)"));
  const i = codegen(parse(lex("if 1 { print 2 } else if 3 { print 4 }")));
  assert.ok(i.indexOf("} else {") < i.indexOf("INT64_C(3)"));
});
