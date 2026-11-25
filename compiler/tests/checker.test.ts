import { test } from 'node:test';
import assert from 'node:assert/strict';
import { lex } from '../src/lexer.ts';
import { parse } from '../src/parser.ts';
import { check } from '../src/checker.ts';
import { resolve } from '../src/resolver.ts';
import { CompileError } from '../src/errors.ts';

// The driver's order: the names first, which the checker is handed.
const accepted = (src: string) => {
    const program = parse(lex(src));
    check(program, resolve(program));
};
const refused = (src: string, message: string, line: number, col: number) =>
    assert.throws(() => accepted(src), (e: unknown) => {
        assert.ok(e instanceof CompileError, String(e));
        assert.deepEqual([e.message, e.line, e.col], [message, line, col]);
        return true;
    });

test('programs', () => {
    accepted('use v5.42;');
    accepted('# a comment\nuse v5.42;\nsay 0;\nsay 9223372036854775807;');
    accepted('use\nv5.42\n;say\n1\n;');
});

test("a program begins 'use v5.42;'", () => {
    const message = "a program begins 'use v5.42;'";
    refused('', message, 1, 1);
    refused('# nothing\n', message, 2, 1);
    refused('\n say 42;', message, 2, 2);
    refused('say 42;\nuse v5.42;', message, 1, 1);
    refused('use v5.36;\nsay 42;', message, 1, 1);
    refused('use v5.42.0;', message, 1, 1);
    refused('use v5;', message, 1, 1);
});

test('the version is said once', () => {
    refused('use v5.42;\nuse v5.42;', "'use v5.42;' here: the version is the first statement, and is said once", 2, 1);
    refused('use v5.42; say 1; use v5.36;', "'use v5.36;' here: the version is the first statement, and is said once", 1, 19);
});

test('the pragmas: a closed list, each written one way, at the top, once (D16, D39)', () => {
    accepted("use v5.42;\nuse utf8;\nuse open ':std', ':encoding(UTF-8)';\nsay 1;");
    accepted('use v5.42;\nuse open ":std", ":encoding(UTF-8)";\nuse utf8;');
    accepted('use v5.42; use open ":s\\x74d", \':encoding(UTF-8)\';');
    const open = "'use open' is written: use open ':std', ':encoding(UTF-8)';";
    refused("use v5.42;\nuse open;", open, 2, 1);
    refused("use v5.42;\nuse open ':std';", open, 2, 1);
    refused("use v5.42;\nuse open ':std', ':utf8';", open, 2, 1);
    refused("use v5.42;\nuse open ':encoding(UTF-8)', ':std';", open, 2, 1);
    refused("use v5.42;\nuse open ':std', ':encoding(UTF-8)', ':std';", open, 2, 1);
    refused("use v5.42;\nuse open ':std', ':encoding(utf-8)';", open, 2, 1);
    refused("use v5.42;\nuse open (':std'), ':encoding(UTF-8)';", open, 2, 1);
    refused("use v5.42;\nuse open ':std' . '', ':encoding(UTF-8)';", open, 2, 1);
    refused("use v5.42;\nuse utf8 'x';", "'use utf8' is written: use utf8;", 2, 1);
    refused('use v5.42;\nuse utf8;\nuse utf8;', "'use utf8' is said once", 3, 1);
    refused("use v5.42;\nsay 1;\nuse utf8;", "'use utf8' goes at the top, after 'use v5.42;' and before anything else", 3, 1);
    refused("use utf8;\nuse v5.42;", "a program begins 'use v5.42;'", 1, 1);
});

test("x with its left operand in brackets, as say's argument, repeats a list to perl (T101)", () => {
    const message = (name: string) => `(...) x as ${name}'s argument repeats a list, to perl: take the brackets off the left operand`;
    // From step 9 that is a list, and in the language (D80).
    accepted('use v5.42;\nsay(("a") x 3);\nprint +("a") x 3;\nsay((("a" . "b")) x 2);\nsay +(+("a") x 2);');
    assert.equal(message('say').length > 0, true);
    refused('use v5.42;\nsay ("a") x 3;', "'x' after say (...): perl takes the brackets for all of say's arguments; bracket the whole expression", 2, 11);
    // In a string's place it is a string that is repeated.
    accepted('use v5.42;\nsay "a" x 3;\nsay(("a") x 3 . "b");\nsay length(("a") x 3);\nsay -("2") x 3;\nsay "" . ("a") x 3;\nsay(("a" x 2) . "");');
    accepted('use v5.42;\nsay(("a" x 3));\nsay "a" x (3);');
});

test('a string, a builtin and its arguments are checked through', () => {
    accepted('use v5.42;\nsay length("abc") . substr("abc", 1, 2) x 2;');
    refused('use v5.42;\nsay substr("abc", 01);', '01 starts with a zero: perl reads that as octal, which the language writes 0o17', 2, 19);
    refused('use v5.42;\nsay length 0xFFFFFFFFF;', '0xFFFFFFFFF is past 32 bits, where perl warns that a literal is not portable', 2, 12);
    refused('use v5.42;\nprint "a" . 9223372036854775808;', '9223372036854775808 is past the largest integer, 9223372036854775807', 2, 13);
});

test('an integer has no leading zero (T24)', () => {
    accepted('use v5.42; say 0;');
    const zero = (text: string) => `${text} starts with a zero: perl reads that as octal, which the language writes 0o17`;
    refused('use v5.42;\nsay 010;', zero('010'), 2, 5);
    refused('use v5.42;\nsay 08;', zero('08'), 2, 5);
    refused('use v5.42; say 00;', zero('00'), 1, 16);
    refused('use v5.42; say 0_17;', zero('0_17'), 1, 16);
    refused('use v5.42; say 00.5;', zero('00.5'), 1, 16);
    refused('use v5.42; say 01e3;', zero('01e3'), 1, 16);
    accepted('use v5.42; say 0.5; say 0e0; say 0x0; say 1e007; say 0.007;');
});

test('every literal in an expression is checked', () => {
    accepted('use v5.42; say -(1 + 2) * +3 % 4;');
    refused('use v5.42;\nsay 1 + 010;', '010 starts with a zero: perl reads that as octal, which the language writes 0o17', 2, 9);
    refused('use v5.42;\nsay -(2 * (3 - 07));', '07 starts with a zero: perl reads that as octal, which the language writes 0o17', 2, 16);
    refused('use v5.42;\nsay 2 ** (1 / 1e999);', '1e999 is past the largest float', 2, 15);
    // The smallest Int has no literal: its digits are past the largest.
    refused('use v5.42;\nsay -9223372036854775808;', '9223372036854775808 is past the largest integer, 9223372036854775807', 2, 6);
    accepted('use v5.42; say -9223372036854775807 - 1;');
});

test('a hex, binary or octal literal is at most 32 bits (D38)', () => {
    const past = (text: string) => `${text} is past 32 bits, where perl warns that a literal is not portable`;
    accepted('use v5.42; say 0xFFFFFFFF; say 0b11111111111111111111111111111111; say 0o37777777777;');
    refused('use v5.42; say 0x100000000;', past('0x100000000'), 1, 16);
    refused('use v5.42; say 0b100000000000000000000000000000000;', past('0b100000000000000000000000000000000'), 1, 16);
    refused('use v5.42; say 0o40000000000;', past('0o40000000000'), 1, 16);
    refused('use v5.42; say 0xFFFF_FFFF_F;', past('0xFFFF_FFFF_F'), 1, 16);
});

test('a decimal literal is at most 250 characters, underscores aside (T91)', () => {
    const long = 'a number of more than 250 characters: perl refuses it as too long';
    accepted(`use v5.42; say 1.${'0'.repeat(248)};`);
    refused(`use v5.42; say 1.${'0'.repeat(249)};`, long, 1, 16);
    accepted(`use v5.42; say 0.${'1_'.repeat(247)}1;`);
    refused(`use v5.42; say 0.${'1_'.repeat(249)}1;`, long, 1, 16);
    refused(`use v5.42; say 1e${'0'.repeat(249)}1;`, long, 1, 16);
    accepted(`use v5.42; say 0x${'0'.repeat(300)}1F;`);
});

test('a float is finite (D37)', () => {
    accepted('use v5.42; say 1.7976931348623157e308; say 1e-400; say 5e-324;');
    refused('use v5.42; say 1e400;', '1e400 is past the largest float', 1, 16);
    refused('use v5.42; say 1.8e308;', '1.8e308 is past the largest float', 1, 16);
});

test('an integer is at most 2^63 - 1 (D23)', () => {
    refused('use v5.42;\nsay 9223372036854775808;', '9223372036854775808 is past the largest integer, 9223372036854775807', 2, 5);
    refused('use v5.42; say 99999999999999999999999999;', '99999999999999999999999999 is past the largest integer, 9223372036854775807', 1, 16);
});

test("the list that say's argument is reaches the right of || and both branches of ? : (T104)", () => {
    // From step 9 each is a list repeated, and in the language (D80);
    // from step 10 after `return` too, where it is list-shaped (D18).
    accepted('use v5.42;\nsay(0 || ("a") x 3);\nsay(1 && ("a") x 3);\nsay(undef // ("a") x 3);\nsay(0 or 1 and ("a") x 3);\nsay 1 ? ("a") x 3 : "b";\nsay 0 ? "b" : 1 ? 2 : (("a")) x 3;\nsay 0 || +("a") x 3;');
    accepted('use v5.42;\nsub f($c) { return $c ? ("a") x 3 : "b"; }');
    accepted('use v5.42;\nsay(("a") x 3 || 0);\nsay((("a") x 3) ? 1 : 2);\nsay(1 xor ("a") x 3);\nsay(!("a") x 3);\nsay(("a") x 3 eq "aaa");\nsay(0 || "" . ("a") x 3);');
});

// What perl says of each is in docs/briefs/claims.py (T114).
test('a statement that only has a value, which perl warns is useless (T114)', () => {
    const message = 'this statement only has a value, and nothing is done with it: perl warns that it is useless';
    refused('use v5.42; my $x = 1; my $y = 1;\n42;', message, 2, 1);
    refused('use v5.42; my $x = 1; my $y = 1;\nlength "abc";', message, 2, 1);
    refused('use v5.42; my $x = 1; my $y = 1;\nsubstr("abc", 1);', message, 2, 1);
    refused('use v5.42; my $x = 1; my $y = 1;\n"abc";', message, 2, 1);
    refused('use v5.42; my $x = 1; my $y = 1;\n(1);', message, 2, 1);
    refused('use v5.42; my $x = 1; my $y = 1;\n- 1;', message, 2, 1);
    refused('use v5.42; my $x = 1; my $y = 1;\n  $x + 1;', message, 2, 3);
    refused('use v5.42; my $x = 1; my $y = 1;\n$x;', message, 2, 1);
    refused('use v5.42; my $x = 1; my $y = 1;\n$x == 1;', message, 2, 1);
    refused('use v5.42; my $x = 1; my $y = 1;\n$x || ($y = 1);', message, 2, 1);
    refused('use v5.42; my $x = 1; my $y = 1;\n1 ? ($x = 1) : 2;', message, 2, 1);
    refused('use v5.42; my $x = 1; my $y = 1;\n{ 42; }', message, 2, 3);
    refused('use v5.42; my $x = 1; my $y = 1;\nif (1) { $x; }', message, 2, 10);
    refused('use v5.42; my $x = 1; my $y = 1;\n$x if 1;', message, 2, 1);
    accepted('use v5.42;\nmy $x;\n$x = 1;\n$x++;\n--$x;\n$x += 2;\n$x ||= 3;\nmy $y = $x;\n$y = $x = 4;');
});

test('where a my may stand: at the head of a statement, or in the test of an if (D56)', () => {
    const here = (name: string) => `my $${name} here: a my begins a statement or a for, or stands in the test of an if or a while, where it is always reached`;
    refused('use v5.42;\nsay my $x;', here('x'), 2, 5);
    refused('use v5.42;\nmy $y;\n$y = my $x = 1;', here('x'), 3, 6);
    refused('use v5.42;\nmy $x = my $y = 1;', here('y'), 2, 9);
    refused('use v5.42;\nmy $x += my $y;', here('y'), 2, 10);
    refused('use v5.42;\nmy $y;\nif (1 && (my $x = $y)) { say 1; }', here('x'), 3, 11);
    refused('use v5.42;\nif (1 ? my $x : 2) { say 1; }', here('x'), 2, 9);
    refused('use v5.42;\nmy $y;\nif ($y ||= my $x) { say 1; }', here('x'), 3, 12);
    refused('use v5.42;\nsay 1 if my $x;', here('x'), 2, 10);
    // T30: perl leaves in the variable what it last held.
    const under = 'my under a modifier: when the test fails, perl leaves in the variable what it last held; declare it in a statement of its own';
    refused('use v5.42;\nmy $x = 1 if 1;', under, 2, 1);
    refused('use v5.42;\nmy $y;\n  my $x unless $y;', under, 3, 3);
    accepted('use v5.42;\nmy $x;\nmy $y = 1;\nif (my $z = $y) { my $w; }\nif ((my $z = $y) > 1) { say 1; }\n'
        + 'if (-(my $z = $y)) { say 1; } elsif (my $v = $y) { say 2; }\nunless (my $u = $y) { say 3; }\n{ my $x = 2; }\nmy $t ||= 5;');
});

// Where perl warns and where it doesn't was asked of perl for each of
// these; the rule is perl's and a little more (T112).
test("'=' where a value is tested, with a constant on its right (D53)", () => {
    const message = "'=' where a value is tested, with nothing but a constant on its right: perl warns that == was meant";
    const at = (src: string, col: number) => refused(`use v5.42;\nmy $x; my $y;\n${src}`, message, 3, col);
    at('if ($x = 5) { say 1; }', 8);
    at('if (($x = 5)) { say 1; }', 9);
    at('if (!($x = 5)) { say 1; }', 10);
    at('if (not $x = 5) { say 1; }', 12);
    at('if (+($x = 5)) { say 1; }', 10);
    at('unless ($x = 5) { say 1; }', 12);
    at('say(($x = 5) ? 1 : 2);', 9);
    at('say(($x = 5) && 1);', 9);
    at('say(!($x = 5) && 1);', 10);
    at('if ($y && ($x = 5)) { say 1; }', 15);
    at('if ($y ? ($x = 1) : 2) { say 1; }', 14);
    at('if ($x = 1 + 2) { say 1; }', 8);
    at('if ($x = length "abc") { say 1; }', 8);
    at('say 1 if $x = 5;', 13);
    at('if (my $z = 5) { say 1; }', 11);
    at('$y = ($x = 5) || 2;', 10);
    at('if (1) { say 1; } elsif ($x = "a") { say 2; }', 29);
    // What perl folds to a constant though a variable is written in it:
    // found by the review of step 5.
    at('if ($x = 0 && $y) { say 1; }', 8);
    at('if ($x = (1 || $y)) { say 1; }', 8);
    at('if ($x = (1 ? 2 : $y)) { say 1; }', 8);
    at('if ($x = ("" // $y)) { say 1; }', 8);
    at('if ($x = -(1 || $y)) { say 1; }', 8);
    at('say "a" if $x = "p" . (1 || $y);', 15);
    at('if ($x = length(1 || $y)) { say 1; }', 8);
    at('if ($x = (1 || $y++)) { say 1; }', 8);
    at('if (my $w = (1 || $y)) { say 1; }', 11);
    for (const src of ['if ($x = $y) { say 1; }', 'if ($x += 5) { say 1; }', 'if ($x ||= 5) { say 1; }', 'if ($x = $y = 5) { say 1; }',
        'if (($x = 5) == 5) { say 1; }', 'say(!($x = 5));', 'say(1 + ($x = 5));', 'if ($x = $y ? 1 : 2) { say 1; }',
        'if ((my $z = 5) > 2) { say 1; }', '$y = !($x = 5);',
        'if ($x = $y && 0) { say 1; }', 'if ($x = $y || 5) { say 1; }', 'if ($x = $y ? 1 : 0) { say 1; }', 'if ($x = 1 + $y) { say 1; }',
        'if ($x = ($y = 5) + 1) { say 1; }']) {
        accepted(`use v5.42;\nmy $x; my $y;\n${src}`);
    }
});

// perl's answers are in docs/briefs/claims.py (T117), and what the
// language makes of the forms it takes is in t/503-late-reads.pl.
test('a later piece of a concatenation may not change what an earlier piece reads (D57)', () => {
    const message = (name: string) =>
        `a later piece of a concatenation changes $${name}, which an earlier piece reads: perl joins the pieces as one operation and reads each late; make the change a statement of its own`;
    const at = (src: string, col: number, name = 'x') => refused(`use v5.42;\nmy $x; my $y;\n${src}`, message(name), 3, col);
    at('say $x . ($x = 5);', 14);
    at('say $x . "a" . $x++;', 18);
    at('say $x . ++$x;', 10);
    at('$x .= $x++;', 9);
    at('say(($y ? $x . "a" : "b") . ($x = 5));', 33);
    at('say(($x || "a") . ($x = 5));', 23);
    at('say length($x) . ($x = 5);', 22);
    at('say "a" . $y . "b" . ($y .= "c");', 26, 'y');
    for (const src of ['say(($x = 5) . $x);', 'say $x . $y++;', 'say $x++ . $y;', 'say $x++ . $x;', 'say $x . ($y = 5) . $y;',
        '$x .= $y++;', 'say(($x = 1) + $x++);', 'say $x . "a";', '$y = ($x . "a") x ($x = 2);']) {
        accepted(`use v5.42;\nmy $x; my $y;\n${src}`);
    }
});

// perl's answers are in docs/briefs/claims.py (T129) and t/566.
test("'.=' of an assignment of a concatenation, which perl never makes (T129)", () => {
    const message = (name: string) =>
        `'.=' of an assignment of a concatenation: perl makes one operation of the three and never assigns $${name}; make the assignment a statement of its own`;
    const at = (src: string, col: number, name = 'y') => refused(`use v5.42;\nmy $x; my $y; my $z;\n${src}`, message(name), 3, col);
    at('$x .= ($y = $z . "a");', 11);
    at('$x .= $y = $z . "a";', 10);
    at('$x .= +(($y = ($z . "a")));', 13);
    at('$x .= (1 ? ($y = $z . "-") : 0);', 16);
    at('$x .= ($y = (0 || ($z . "a")));', 11);
    at('say($x .= ($y = "k" . $z));', 15);
    at('$x .= ($y = $z . "a") if $z;', 11);
    for (const src of ['$x .= ($y .= $z);', '$x = $x . ($y = $z . "a");', '$x .= ($y = $z . "a") . "b";', '$x .= "b" . ($y = $z . "a");',
        '$x .= ($y = $z x 2);', '$x .= ($y = $z);', '$x .= ($y = $z . "a") x 1;', '$x .= ($y = lc($z . "a"));', '$x += ($y = $z . 1);']) {
        accepted(`use v5.42;\nmy $x; my $y; my $z;\n${src}`);
    }
});

test('use and the pragmas are at the top, not in a block', () => {
    refused('use v5.42;\n{ use v5.42; }', "'use v5.42;' here: the version is the first statement, and is said once", 2, 3);
    refused('use v5.42;\nif (1) { use utf8; }', "'use utf8' goes at the top, after 'use v5.42;' and before anything else", 2, 10);
});

test('the parts of a for: what could be statements, and a my in the first only (D60)', () => {
    const at = (src: string, message: string, col: number) => refused(`use v5.42;\nmy $i; my $j;\n${src}`, message, 3, col);
    const useless = 'this part of the for only has a value, and nothing is done with it: perl warns that it is useless';
    at('for ($i + 1; ; ) { }', useless, 9);
    at('for (; ; $i) { }', useless, 10);
    at('for ($i = 0, 5; ; ) { }', useless, 14);
    at('for (; ; $i++, $j == 1) { }', useless, 19);
    at('for (; ; my $k = 1) { }', 'my $k in the third part of a for: a my is in the first part, and is one variable for the whole loop', 10);
    at('for (; (my $c = $i) < 3; ) { }', 'my $c here: a my begins a statement or a for, or stands in the test of an if or a while, where it is always reached', 9);
    at('for ($j = my $k = 1; ; ) { }', 'my $k here: a my begins a statement or a for, or stands in the test of an if or a while, where it is always reached', 11);
    for (const src of ['for (my $k = 0, my $m = $i; $k < $m; $k++, $m--) { }', 'for (my $k; ; ) { last; }', 'for ($i = 0, $j = 1; ; $i += 1, $j .= "a") { last; }',
        'for (;;) { last; }', 'for (my $k = 0; $k < 3; ++$k) { my $k = 1; }']) {
        accepted(`use v5.42;\nmy $i; my $j;\n${src}`);
    }
});

test("a loop's test is a test, and a my under while is as one under if (D53, T119)", () => {
    const tested = "'=' where a value is tested, with nothing but a constant on its right: perl warns that == was meant";
    const at = (src: string, message: string, col: number) => refused(`use v5.42;\nmy $i; my $j;\n${src}`, message, 3, col);
    at('while ($i = 5) { }', tested, 11);
    at('until ($i = 5) { }', tested, 11);
    at('for (; $i = 5; ) { }', tested, 11);
    at('$i++ while $i = 0;', tested, 15);
    at('while (!($i = 5)) { }', tested, 13);
    at('while ($i = 0 && $j) { }', tested, 11);
    at('my $x = 5 while $i;', 'my under a modifier: when the test fails, perl leaves in the variable what it last held; declare it in a statement of its own', 1);
    at('say 1 while my $x;', 'my $x here: a my begins a statement or a for, or stands in the test of an if or a while, where it is always reached', 13);
    at('while ($i) { use utf8; }', "'use utf8' goes at the top, after 'use v5.42;' and before anything else", 14);
    at('while ($i) { $i + 1; }', 'this statement only has a value, and nothing is done with it: perl warns that it is useless', 14);
    for (const src of ['while ((my $d = $i) < 3) { }', 'until (my $d = $i) { }', 'while ($i = $j) { }', 'while (1) { last; }', '$i++ until $i > 3;',
        'while ($i += 1) { last; }', 'for (; $i = $j; ) { last; }']) {
        accepted(`use v5.42;\nmy $i; my $j;\n${src}`);
    }
});
