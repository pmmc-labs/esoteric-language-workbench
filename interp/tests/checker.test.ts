import { test } from "node:test";
import assert from "node:assert/strict";
import { read } from "../src/reader.ts";
import { check } from "../src/checker.ts";
import { CheckError } from "../src/errors.ts";

// The error before running for a program, as `L:C message`, or "ok".
export const checked = (src: string) => {
  try { check(read(src)); return "ok"; } catch (e) {
    assert.ok(e instanceof CheckError, String(e));
    return `${e.line}:${e.col} ${e.message}`;
  }
};

test("arithmetic with two operands is fine", () => {
  assert.equal(checked("(+ (* 6 7) (- 10 (/ 7 2)))"), "ok");
  assert.equal(checked("(% 1 2)"), "ok");
});

test("an operator with other than two operands (D3)", () => {
  assert.equal(checked("(+ 1 2 3)"), "1:1 + takes 2 arguments, not 3");
  assert.equal(checked("(- 1)"), "1:1 - takes 2 arguments, not 1");
  assert.equal(checked("(*)"), "1:1 * takes 2 arguments, not 0");
  assert.equal(checked("(+ 1\n  (/ 1 2 3))"), "2:3 / takes 2 arguments, not 3");
});

test("an unknown name, as an operator or on its own (D7)", () => {
  assert.equal(checked("(foo 1 2)"), "1:2 unknown name foo");
  assert.equal(checked("x"), "1:1 unknown name x");
  assert.equal(checked("(+ 1 y)"), "1:6 unknown name y");
});

test("a list whose head isn't an operator", () => {
  assert.equal(checked("()"), "1:1 a list must start with an operator");
  assert.equal(checked("(1 2 3)"), "1:1 a list must start with an operator");
  assert.equal(checked("((+ 1 2) 3 4)"), "1:1 a list must start with an operator");
});

test("an error in a branch nothing evaluates is still found", () => {
  assert.equal(checked("(+ 1 (foo))"), "1:7 unknown name foo");
});

test("booleans, comparisons and if", () => {
  assert.equal(checked("(if (< 1 2) #true #false)"), "ok");
  assert.equal(checked("(== #true 1)"), "ok");
  assert.equal(checked("#true"), "ok");
});

test("an if with other than three parts, even in a branch never taken (D13, D28)", () => {
  assert.equal(checked("(if #true 1)"), "1:1 if takes 3 arguments, not 2");
  assert.equal(checked("(if)"), "1:1 if takes 3 arguments, not 0");
  assert.equal(checked("(if #true 1 2 3)"), "1:1 if takes 3 arguments, not 4");
  assert.equal(checked("(if #false (+ 1 2 3) 0)"), "1:12 + takes 2 arguments, not 3");
  assert.equal(checked("(if #true 0 (if 1 2))"), "1:13 if takes 3 arguments, not 2");
});

test("if on its own is an unknown name, and #true is no operator", () => {
  assert.equal(checked("(+ 1 if)"), "1:6 unknown name if");
  assert.equal(checked("(#true 1 2)"), "1:1 a list must start with an operator");
  assert.equal(checked("#maybe"), "1:1 unknown name #maybe");
});

test("the bit operations take two arguments", () => {
  assert.equal(checked("(bit/and 1 2)"), "ok");
  assert.equal(checked("(bit/not 1)"), "1:2 unknown name bit/not");
  assert.equal(checked("(bit/shl 1)"), "1:1 bit/shl takes 2 arguments, not 1");
});

test("** takes two arguments", () => {
  assert.equal(checked("(** 2 3)"), "ok");
  assert.equal(checked("(** 2)"), "1:1 ** takes 2 arguments, not 1");
});

test("within takes two parts, checked in an untaken branch too (D24, D28)", () => {
  assert.equal(checked("(within 1 2)"), "ok");
  assert.equal(checked("(within)"), "1:1 within takes 2 arguments, not 0");
  assert.equal(checked("(within 5)"), "1:1 within takes 2 arguments, not 1");
  assert.equal(checked("(within 1 2 3)"), "1:1 within takes 2 arguments, not 3");
  assert.equal(checked("(if #false (within 1) 0)"), "1:12 within takes 2 arguments, not 1");
  assert.equal(checked("(+ 1 within)"), "1:6 unknown name within");
});

// The program's shape: definitions, then one expression (D31).
test("a program is definitions and then one expression (D31)", () => {
  assert.equal(checked("1 2"), "1:3 a second expression after the program's expression");
  assert.equal(checked("(+ 1 2) (+ 3 4)"), "1:9 a second expression after the program's expression");
  assert.equal(checked("(def (f) 1) 2 3"), "1:15 a second expression after the program's expression");
  assert.equal(checked("1 (def (f) 1)"), "1:3 a definition after the expression");
  assert.equal(checked("(def (f) 1)"), "1:1 a program of definitions needs an expression after them");
  assert.equal(checked("(def (f) 1) (f)"), "ok");
});

test("definitions: two parts, a name, not a reserved name, no repeats (D31)", () => {
  assert.equal(checked("(def (f) 1) 0"), "ok");
  assert.equal(checked("(def f) 0"), "1:1 def takes 2 arguments, not 1");
  assert.equal(checked("(def (f) 1 2) 0"), "1:1 def takes 2 arguments, not 3");
  assert.equal(checked("(def 1 2) 0"), "1:6 a definition's first part is its name and parameters, in a list");
  assert.equal(checked("(def () 2) 0"), "1:6 a definition needs a name");
  assert.equal(checked("(def ((f)) 2) 0"), "1:7 a definition needs a name");
  assert.equal(checked("(def (+ x) x) 0"), "1:7 + is not a name for a function");
  assert.equal(checked("(def (if x) x) 0"), "1:7 if is not a name for a function");
  assert.equal(checked("(def (within x) x) 0"), "1:7 within is not a name for a function");
  assert.equal(checked("(def (def x) x) 0"), "1:7 def is not a name for a function");
  assert.equal(checked("(def (f) 1) (def (f) 2) 0"), "1:19 two definitions of f");
});

test("parameters: names, not reserved, not a function's, no repeats (D31)", () => {
  assert.equal(checked("(def (f a b) a) 0"), "ok");
  assert.equal(checked("(def (f 1) 1) 0"), "1:9 a parameter is a name, not a number or boolean");
  assert.equal(checked("(def (f #true) 1) 0"), "1:9 a parameter is a name, not a number or boolean");
  assert.equal(checked("(def (f +) 1) 0"), "1:9 + is not a name for a parameter");
  assert.equal(checked("(def (f if) 1) 0"), "1:9 if is not a name for a parameter");
  assert.equal(checked("(def (f a a) 1) 0"), "1:11 two parameters named a");
  assert.equal(checked("(def (f g) 1) (def (g) 2) 0"), "1:9 g is the name of a function");
  assert.equal(checked("(def (f f) 1) 0"), "1:9 f is the name of a function");
});

test("calls: arity, unknown names, functions and parameters used wrongly (D31)", () => {
  assert.equal(checked("(def (f a b) (+ a b)) (f 1 2)"), "ok");
  assert.equal(checked("(def (f a b) (+ a b)) (f 1 2 3)"), "1:23 f takes 2 arguments, not 3");
  assert.equal(checked("(def (f a b) (+ a b)) (f 1)"), "1:23 f takes 2 arguments, not 1");
  assert.equal(checked("(def (f) 1) (g)"), "1:14 unknown name g");
  assert.equal(checked("(def (f) 1) (+ f 1)"), "1:16 f is a function, not a value");
  assert.equal(checked("(def (f x) (x 1)) 0"), "1:13 x is a parameter, not a function");
  assert.equal(checked("(def (f x) (+ x y)) 0"), "1:17 unknown name y");
  assert.equal(checked("(def (f x) x) x"), "1:15 unknown name x");
});

test("a function's body is checked whether or not it is called (D7, D28)", () => {
  assert.equal(checked("(def (f) (+ 1 2 3)) 0"), "1:10 + takes 2 arguments, not 3");
});

test("a definition inside a body or the expression is an error (D31)", () => {
  assert.equal(checked("(def (f) (def (g) 1)) 0"), "1:10 a definition is only at the top of the program");
  assert.equal(checked("(+ 1 (def (g) 1))"), "1:6 a definition is only at the top of the program");
});

test("every definition sees every other, in any order (D31)", () => {
  assert.equal(checked("(def (a) (b)) (def (b) 1) (a)"), "ok");
});
