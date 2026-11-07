import { test } from "node:test";
import assert from "node:assert/strict";
import { run } from "./helper.ts";

test("arithmetic, nested (D3, D5)", () => {
  assert.equal(run("(+ (* 6 7) (- 10 (/ 7 2)))"), "49");
  assert.equal(run("(/ -7 2)"), "-3");
  assert.equal(run("(% -7 2)"), "-1");
  assert.equal(run("(% 7 -2)"), "1");
  assert.equal(run("(/ 7 -2)"), "-3");
});

test("overflow at both edges, and in a quotient (D4)", () => {
  assert.equal(run("(+ 4611686018427387903 1)"), "fault: overflow");
  assert.equal(run("(- -4611686018427387904 1)"), "fault: overflow");
  assert.equal(run("(* 3037000500 3037000500)"), "fault: overflow");
  assert.equal(run("(/ -4611686018427387904 -1)"), "fault: overflow");
  assert.equal(run("(- 0 -4611686018427387904)"), "fault: overflow");
  assert.equal(run("(+ 4611686018427387903 -4611686018427387904)"), "-1");
  assert.equal(run("(% -4611686018427387904 -1)"), "0");
});

test("division by zero (D6)", () => {
  assert.equal(run("(/ 1 0)"), "fault: division by zero");
  assert.equal(run("(% 1 0)"), "fault: division by zero");
});

test("a deep right-nested program evaluates", () => {
  const n = 900;
  assert.equal(run("(+ 1 ".repeat(n) + "0" + ")".repeat(n)), String(n));
});

test("booleans print as written; comparisons give booleans (D11, D12)", () => {
  assert.equal(run("#true"), "#true");
  assert.equal(run("(< 1 2)"), "#true");
  assert.equal(run("(>= 1 2)"), "#false");
  assert.equal(run("(<= -4611686018427387904 4611686018427387903)"), "#true");
});

test("== and != on any two values, never coercing (D12)", () => {
  assert.equal(run("(== 1 #true)"), "#false");
  assert.equal(run("(== 0 #false)"), "#false");
  assert.equal(run("(!= 0 #false)"), "#true");
  assert.equal(run("(== #true #true)"), "#true");
  assert.equal(run("(== (+ 1 1) 2)"), "#true");
  assert.equal(run("(!= 1 1)"), "#false");
});

test("arithmetic and orderings fault on a boolean (D11)", () => {
  assert.equal(run("(+ 1 #true)"), "fault: not an integer");
  assert.equal(run("(< #false 1)"), "fault: not an integer");
  assert.equal(run("(+ 1 (if #true #false 0))"), "fault: not an integer");
});

test("if: a boolean test, one branch evaluated (D13)", () => {
  assert.equal(run("(if #true 1 (/ 1 0))"), "1");
  assert.equal(run("(if #false (/ 1 0) 2)"), "2");
  assert.equal(run("(if (- 1 1) 1 2)"), "fault: not a boolean");
  assert.equal(run("(if #true #false 3)"), "#false");
});

test("evaluation is left to right (D25)", () => {
  assert.equal(run("(+ (/ 1 0) (+ #true 1))"), "fault: division by zero");
  assert.equal(run("(+ (+ #true 1) (/ 1 0))"), "fault: not an integer");
});

test("bit and, or, xor on the sign-extended value (D15)", () => {
  assert.equal(run("(bit/and -1 7)"), "7");
  assert.equal(run("(bit/or -8 1)"), "-7");
  assert.equal(run("(bit/xor -1 0)"), "-1");
  assert.equal(run("(bit/xor -4611686018427387904 4611686018427387903)"), "-1");
  assert.equal(run("(bit/and -4611686018427387904 -1)"), "-4611686018427387904");
});

test("shifts (D16)", () => {
  assert.equal(run("(bit/shl 1 61)"), "2305843009213693952");
  assert.equal(run("(bit/shl 1 62)"), "fault: overflow");
  assert.equal(run("(bit/shl -1 62)"), "-4611686018427387904");
  assert.equal(run("(bit/shl 0 62)"), "0");
  assert.equal(run("(bit/shr -7 1)"), "-4");
  assert.equal(run("(bit/shr 7 1)"), "3");
  assert.equal(run("(bit/shr -1 62)"), "-1");
  assert.equal(run("(bit/shr 4611686018427387903 62)"), "0");
});

test("a count outside 0 to 62 faults bad shift (D16)", () => {
  assert.equal(run("(bit/shl 1 63)"), "fault: bad shift");
  assert.equal(run("(bit/shl 1 -1)"), "fault: bad shift");
  assert.equal(run("(bit/shr 7 63)"), "fault: bad shift");
  assert.equal(run("(bit/shr 7 -1)"), "fault: bad shift");
  assert.equal(run("(bit/shr 7 4611686018427387903)"), "fault: bad shift");
});

test("a boolean faults not an integer, and that is reported before a bad count", () => {
  assert.equal(run("(bit/and #true 1)"), "fault: not an integer");
  assert.equal(run("(bit/shl #true 1)"), "fault: not an integer");
  assert.equal(run("(bit/shl #true 99)"), "fault: not an integer");
  assert.equal(run("(bit/shr 1 #false)"), "fault: not an integer");
});

test("exponentiation (D18, D19)", () => {
  assert.equal(run("(** 2 10)"), "1024");
  assert.equal(run("(** -3 3)"), "-27");
  assert.equal(run("(** 2 61)"), "2305843009213693952");
  assert.equal(run("(** -2 62)"), "fault: overflow");
  assert.equal(run("(** -2 61)"), "-2305843009213693952");
  assert.equal(run("(** 2 62)"), "fault: overflow");
  assert.equal(run("(** 2 4611686018427387903)"), "fault: overflow");
  assert.equal(run("(** 3 39)"), "4052555153018976267");
  assert.equal(run("(** 3 40)"), "fault: overflow");
});

test("a ** 0 is 1, 0 ** 0 too; 0, 1 and -1 to any power (D19)", () => {
  assert.equal(run("(** 0 0)"), "1");
  assert.equal(run("(** 4611686018427387903 0)"), "1");
  assert.equal(run("(** -4611686018427387904 0)"), "1");
  assert.equal(run("(** 0 4611686018427387903)"), "0");
  assert.equal(run("(** 1 4611686018427387903)"), "1");
  assert.equal(run("(** -1 4611686018427387903)"), "-1");
  assert.equal(run("(** -1 4611686018427387902)"), "1");
});

test("a negative exponent faults bad exponent, whatever the base (D19)", () => {
  assert.equal(run("(** 2 -1)"), "fault: bad exponent");
  assert.equal(run("(** 1 -1)"), "fault: bad exponent");
  assert.equal(run("(** 0 -4611686018427387904)"), "fault: bad exponent");
});

test("a boolean to ** faults not an integer (D19)", () => {
  assert.equal(run("(** #true 2)"), "fault: not an integer");
  assert.equal(run("(** 2 #false)"), "fault: not an integer");
});

test("within: n operations allowed, the next faults (D20 to D22)", () => {
  assert.equal(run("(within 3 (+ (* 2 3) (- 10 4)))"), "12");
  assert.equal(run("(within 2 (+ (* 2 3) (- 10 4)))"), "fault: budget spent");
  assert.equal(run("(within 0 42)"), "42");
  assert.equal(run("(within 1 (< 1 2))"), "#true");
  assert.equal(run("(within 1 (** 1 4611686018427387903))"), "1");
});

test("the charge is after the operands and before the checks (D22)", () => {
  assert.equal(run("(within 1 (+ (/ 1 0) 2))"), "fault: division by zero");
  assert.equal(run("(within 0 (/ 1 0))"), "fault: budget spent");
  assert.equal(run("(within 0 (+ #true 1))"), "fault: budget spent");
  assert.equal(run("(within 0 (== 1 2))"), "fault: budget spent");
});

test("if and within are free, an untaken branch costs nothing (D21)", () => {
  assert.equal(run("(within 0 (if #true (within 0 7) (/ 1 0)))"), "7");
  assert.equal(run("(within 2 (if (< 1 2) (+ 40 2) (+ (+ 1 1) (+ 1 1))))"), "42");
});

test("budgets nest and every one applies (D23)", () => {
  assert.equal(run("(within 1 (within 5 (+ (+ 1 2) 3)))"), "fault: budget spent");
  assert.equal(run("(within 5 (within 1 (+ (+ 1 2) 3)))"), "fault: budget spent");
  assert.equal(run("(within 3 (+ (within 5 (+ (+ 1 2) 3)) 4))"), "10");
  assert.equal(run("(within 2 (+ (within 5 (+ (+ 1 2) 3)) 4))"), "fault: budget spent");
  // After an inner within ends, the outer's limit is back in force.
  assert.equal(run("(within 3 (+ (within 1 (+ 1 1)) (+ 1 1)))"), "4");
  assert.equal(run("(within 2 (+ (within 1 (+ 1 1)) (+ 1 1)))"), "fault: budget spent");
  assert.equal(run("(within 4611686018427387903 (within 4611686018427387903 (+ 1 1)))"), "2");
});

test("the budget is an expression, charged to the budgets around (D24)", () => {
  assert.equal(run("(within 2 (within (+ 1 1) (* 3 4)))"), "12");
  assert.equal(run("(within 1 (within (+ 1 1) (* 3 4)))"), "fault: budget spent");
  assert.equal(run("(within #true 1)"), "fault: not an integer");
  assert.equal(run("(within -1 (/ 1 0))"), "fault: bad budget");
  assert.equal(run("(within (- 0 1) 1)"), "fault: bad budget");
});

test("a program outside every within counts nothing (D23)", () => {
  assert.equal(run("(+ (+ (+ 1 1) (+ 1 1)) (+ (+ 1 1) (+ 1 1)))"), "8");
});

test("each run starts with a fresh budget", () => {
  assert.equal(run("(within 1 (+ 1 1))"), "2");
  assert.equal(run("(within 1 (+ 1 1))"), "2");
});

test("strings: length, index, order, code and char by code points (D31, D33)", async () => {
  const { run } = await import("./helper.ts");
  assert.equal(run('(str/len "a😀e\\u{301}")'), "4");
  assert.equal(run('(str/at "a😀" 1)'), '"😀"');
  assert.equal(run('(str/lt "\\u{FFFF}" "\\u{10000}")'), "#true");
  assert.equal(run('(str/lt "ab" "a")'), "#false");
  assert.equal(run('(str/code "😀")'), "128512");
  assert.equal(run("(str/char 128512)"), '"😀"');
  assert.equal(run('(== "é" "e\\u{301}")'), "#false");
});

test("strings: faults and their order (D33)", async () => {
  const { run } = await import("./helper.ts");
  assert.equal(run('(str/at "ab" 7)'), "fault: bad index");
  assert.equal(run('(str/at 5 #true)'), "fault: not a string");
  assert.equal(run('(str/at "ab" #true)'), "fault: not an integer");
  assert.equal(run('(str/len 1)'), "fault: not a string");
  assert.equal(run('(str/code "")'), "fault: not a character");
  assert.equal(run('(str/char #true)'), "fault: not an integer");
  assert.equal(run('(str/char 55296)'), "fault: not a character");
  assert.equal(run('(str/cat "a" 1)'), "fault: not a string");
  assert.equal(run('(+ "a" 1)'), "fault: not an integer");
  assert.equal(run('(== "1" 1)'), "#false");
});

test("strings print per D32 and are an operation each (D21, D32)", async () => {
  const { run } = await import("./helper.ts");
  assert.equal(run('"a\\"\\\\\\n\\t\\u{7}\\u{7f}\\u{80}\\u{2028}é"'), '"a\\"\\\\\\n\\t\\u{7}\\u{7f}\u0080 é"');
  assert.equal(run('(within 1 (str/len "a"))'), "1");
  assert.equal(run('(within 0 (str/len "a"))'), "fault: budget spent");
  assert.equal(run('(within 0 "x")'), '"x"');
});
