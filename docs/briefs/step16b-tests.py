#!/usr/bin/env python3
# Writes step 16b's fault and refusal tests from tables written by hand.
# A fault test is a program, what it prints before the fault, and the
# fault's message and line; a refusal is a program, the text the message
# points at (its column is counted here) and the message. Nothing here
# asks the compiler. What perl does with each is in its comment, pasted
# from perl 5.42.
#
#     python3 docs/briefs/step16b-tests.py 2720 2760
import sys

F = []   # faults: name, why, body, printed before, message, the fault's line in the body
R = []   # refusals: name, why, body, at, message


def f(name, why, body, before, message, line):
    F.append((name, why, body, before, message, line))


def r(name, why, body, at, message, nth=1):
    R.append((name, why, body, at, message, nth))


OUTSIDE = 'a number outside the integers where a whole number is wanted'
UNSIGNED = 'a number outside 64 bits where a format wants a whole number'
NEGZERO = 'a negative zero to %e, %f or %g: perl prints 0 or -0 by what the zero was used as'

# ---- faults (D126, D127, D131)
f('missing-argument', 'perl prints a- and warns: Missing argument in sprintf (T270).', 'say "before";\nsay sprintf("%s-%s", "a");', 'before\n', 'missing argument in sprintf', 2)
f('redundant-argument', 'perl prints a and warns: Redundant argument in sprintf (T270).', 'say "before";\nsay sprintf("%s", "a", "b");', 'before\n', 'redundant argument in sprintf', 2)
f('redundant-argument-no-conversion', 'perl prints abc and warns: Redundant argument in sprintf.', 'say sprintf("abc", 1);', '', 'redundant argument in sprintf', 1)
f('missing-argument-from-an-array', 'perl prints 1-2- and warns: Missing argument.', 'my @l = (1, 2);\nsay sprintf("%s-%s-%s", @l);', '', 'missing argument in sprintf', 2)
f('missing-argument-for-a-star', 'perl prints 5 and warns: Missing argument.', 'say sprintf("%*d", 5);', '', 'missing argument in sprintf', 1)
f('printf-missing-argument', 'perl prints | and warns: Missing argument in printf (T270).', 'printf("%s|\\n");', '', 'missing argument in printf', 1)
f('printf-redundant-argument', 'perl prints abc and warns: Redundant argument in printf (T270).', 'printf("abc\\n", 1);', '', 'redundant argument in printf', 1)
f('d-of-2-to-the-63', 'perl prints -9223372036854775808 (T265).', 'say sprintf("%d", 9223372036854775807);\nsay sprintf("%d", 9223372036854775808.0);', '9223372036854775807\n', OUTSIDE, 2)
f('d-below-the-ints', 'perl prints -9223372036854775808, clamped.', 'say sprintf("%d", -9223372036854775808.0);\nsay sprintf("%d", -9223372036854777856.0);', '-9223372036854775808\n', OUTSIDE, 2)
f('d-of-1e30', 'perl prints -1 (T265).', 'say sprintf("%d", 1e30);', '', OUTSIDE, 1)
f('x-of-2-to-the-64', 'perl prints ffffffffffffffff, clamped (T265).', 'say sprintf("%x", 18446744073709549568.0);\nsay sprintf("%x", 18446744073709551616.0);', 'fffffffffffff800\n', UNSIGNED, 2)
f('u-below-the-ints', 'perl prints 9223372036854775808: -2^63 - 2048 clamped.', 'say sprintf("%u", -9223372036854777856.0);', '', UNSIGNED, 1)
f('c-of-a-surrogate', 'perl makes the surrogate, and warns when it is printed.', 'say sprintf("%c", 0xD800);', '', 'not a character', 1)
f('c-below-zero', 'perl dies: Use of code point 0xFFFFFFFFFFFFFFFF is not allowed.', 'say sprintf("%c", -1);', '', 'not a character', 1)
f('c-past-unicode', 'perl makes the character, and warns when it is printed.', 'say sprintf("%c", 0x110000);', '', 'not a character', 1)
f('g-of-a-negative-zero', 'perl prints -0 here, and 0 when the zero has been an integer (T267).', 'my $z = 0.0;\nsay sprintf("%g", $z);\nsay sprintf("%g", -$z);', '0\n', NEGZERO, 3)
f('e-of-a-negative-zero-string', 'perl prints -0.000000e+00, and 0.000000e+00 after "-0" + 0 (T282).', 'say sprintf("%e", "-0");', '', NEGZERO, 1)
f('f-of-a-negative-zero-string', 'perl prints -0.0 (T282).', 'say sprintf("%.1f", " -0.0");', '', NEGZERO, 1)
f('s-of-undef', 'perl prints nothing and warns: Use of uninitialized value in sprintf.', 'my $u;\nsay sprintf("[%s]", $u);', '', 'undef where a string is wanted', 2)
f('d-of-undef', 'perl prints 0 and warns: Use of uninitialized value in sprintf.', 'my $u;\nsay sprintf("%d", $u);', '', 'undef where a number is wanted', 2)
f('star-of-undef', 'perl takes 0 and warns: Use of uninitialized value in sprintf.', 'my $u;\nsay sprintf("%*s", $u, "a");', '', 'undef where a number is wanted', 2)
f('d-of-a-string-no-number', 'perl prints 0 and warns: Argument "abc" isn\'t numeric in sprintf.', 'say sprintf("%d", "abc");', '', 'not a numeric string', 1)
f('d-of-a-split-string', 'perl cuts it to 1 or to 2 by what the string was used as before.', 'say sprintf("%d", "1.99999999999999999");', '', 'a string with a point this close to the next whole number has two values in perl', 1)
f('s-of-a-whole-float', 'perl prints 1e+15; the language prints no whole Num from 10^15 (D36).', 'say sprintf("%s", 1e15);', '', 'a whole float this size prints two ways in perl (add 0 to print the integer)', 1)
f('star-of-2-to-the-62', 'perl dies: Integer overflow in format string for sprintf (T283); from 2^31 it makes a string that long.', 'say sprintf("%.*f", 2, 1.5);\nsay length sprintf("%*d", 4611686018427387904, 1);', '1.50\n', "a format's width or precision of 2^31 or more", 2)
f('star-of-minus-2-to-the-62', 'perl dies: Integer overflow in format string for sprintf.', 'say length sprintf("%*d", -4611686018427387904, 1);', '', "a format's width or precision of 2^31 or more", 1)
# (A string past 2^31 - 1 characters, `formatted string too long`, is tested
# from C, runtime/tests/format.c: no test asks perl for one.)
f('printf-past-ascii-without-use-open', 'perl prints one byte for it, where the language would print two (D39).', 'printf("%s\\n", chr(233));', '', "a character past ASCII printed without 'use open'", 1)

# ---- refusals (D124, D125, D131)
NOTLIT = lambda n: f"{n}'s format is a string literal with no variable in it (D124): perl takes the first value of an array, or a string made as the program runs, for one (T274)"
r('format-an-array', 'perl takes the count for the format: 3 (T22, T274).', 'my @a = ("%s-%s", 2, 3);\nsay sprintf(@a);', '@a)', NOTLIT('sprintf'))
r('format-a-variable', 'perl takes it: 3.', 'my $f = "%d";\nsay sprintf($f, 3);', '$f,', NOTLIT('sprintf'))
r('format-interpolated', 'perl reads the % in $p as a conversion: 5.', 'my $p = "%d";\nsay sprintf("<$p>", 5);', '"<$p>"', NOTLIT('sprintf'))
r('format-a-qw', 'perl takes the first word for the format: a-b.', 'say sprintf(qw(%s-%s a b));', 'qw(', NOTLIT('sprintf'))
r('printf-format-a-variable', 'perl takes it: 3.', 'my $f = "%d\\n";\nprintf($f, 3);', '$f,', NOTLIT('printf'))
r('format-none', 'perl prints $_, undef, and warns.', 'printf();', '();', 'printf() with nothing to print: perl prints $_')
B = lambda what: f"{what} in sprintf's format"
r('percent-at-the-end', 'perl prints abc% and warns: Invalid conversion in sprintf: end of string (T270).', 'say sprintf("abc%");', '"abc%"', B("a '%' at the end, which perl warns of (T270): write %% for the character"))
r('unknown-conversion', 'perl prints %y and warns: Invalid conversion (T270).', 'say sprintf("%y", 1);', '"%y"', B('%y, which is no conversion: perl prints it as it is and warns (T270),'))
r('unfinished-conversion', 'perl prints %5 and warns: Invalid conversion.', 'say sprintf("%5");', '"%5"', B('an unfinished conversion, %5, which perl prints as it is and warns of (T270),'))
r('i', 'perl takes %i for %d: 3.', 'say sprintf("%i", 3);', '"%i"', B("%i, perl's other spelling of %d: write that,"))
r('upper-d', 'perl takes %D for %ld: 4.', 'say sprintf("%D", 4);', '"%D"', B("%D, perl's other spelling of %ld, which is %d: write that,"))
r('upper-f', 'perl takes %F for %f: 1.500000.', 'say sprintf("%F", 1.5);', '"%F"', B("%F, perl's other spelling of %f: write that,"))
r('size-letter', 'perl ignores it: 1.', 'say sprintf("%ld", 1);', '"%ld"', B("a size letter, %l..., which perl ignores: leave it out,"))
r('vector', 'perl prints 49.46.50 (T276).', 'say sprintf("%vd", "1.2");', '"%vd"', B("%v, which is not in the language (a version string's format; T276),"))
r('n', 'perl dies: Modification of a read-only value attempted (T276).', 'say sprintf("%n", 1);', '"%n"', B('%n, which is not in the language (a write to its argument; T276),'))
r('p', 'perl prints an address.', 'say sprintf("%p", 1);', '"%p"', B('%p, which is not in the language (an address; T276),'))
r('hex-float', 'perl prints 0x1p+0.', 'say sprintf("%a", 1);', '"%a"', B('%a, which is not in the language (a hex float; T276),'))
r('argument-by-number', 'perl prints b a (T276).', 'say sprintf("%2\\$s %1\\$s", "a", "b");', '"%2', B('an argument by its number, %2$s..., which is not in the language (T276),'))
r('width-too-large', 'perl runs out of memory as it compiles (T271).', 'say sprintf("%99999999999d", 1);', '"%9', B('a width or precision of 2^31 or more, 99999999999, which perl does not survive (T271),'))
r('precision-too-large', 'perl prints garbage for %.2147483648d.', 'say sprintf("%.2147483648d", 1);', '"%.', B('a width or precision of 2^31 or more, 2147483648, which perl does not survive (T271),'))
r('width-on-percent', 'perl pads it: four blanks and %.', 'say sprintf("%5%");', '"%5%"', B('a flag, width or precision on %%, %5%, which perl pads: write the padding,'))
r('width-on-c', 'perl pads a wide character by its bytes: no blank before it (T277).', 'say sprintf("%3c", 0x263A);', '"%3c"', B('a width or a precision on %c: perl pads a character past U+00FF by its bytes (T277), and %.0c is nothing,'))
r('precision-on-c', 'perl prints nothing for %.0c.', 'say sprintf("[%.0c]", 65);', '"[%.0c]"', B('a width or a precision on %c: perl pads a character past U+00FF by its bytes (T277), and %.0c is nothing,'))
r('flag-on-c', 'perl ignores it: A.', 'say sprintf("%+c", 65);', '"%+c"', B("the flag '+' on %c, which perl ignores,"))
r('plus-on-s', 'perl ignores it: ab.', 'say sprintf("%+s", "ab");', '"%+s"', B("the flag '+' on %s, which perl ignores there,"))
r('hash-on-s', 'perl ignores it: ab.', 'say sprintf("%#s", "ab");', '"%#s"', B("the flag '#' on %s, which perl ignores there,"))
r('star-then-digits', 'perl prints %*3d and warns: Invalid conversion.', 'say sprintf("%*3d", 5, 3);', '"%*3d"', B('%*3, which is no conversion: perl prints it as it is and warns (T270),'))
r('printf-bad-format', 'perl prints %y and warns: Invalid conversion in printf.', 'printf("%y\\n", 1);', '"%y', "%y, which is no conversion: perl prints it as it is and warns (T270), in printf's format")
r('printf-to-a-handle', 'perl prints a to stdout; a handle is step 21.', 'printf STDOUT "%s\\n", "a";', 'STDOUT', "expected a value, found 'STDOUT'")
r('sprintf-sliced', 'perl does not compile it: syntax error.', 'say sprintf("%s", 1)[0];', '[0]', "'[' after sprintf(...): perl does not compile it; bracket the whole, (sprintf(...))[...]")
r('printf-as-a-value', 'perl gives 1, what printf returns.', 'my $r = printf("%s\\n", "b");', 'printf', 'printf is a statement, and has no value')


def write(first_fault, first_refusal):
    n = first_fault
    for name, why, body, before, message, line in F:
        program = f'# kind: fault\n# {why}\nuse v5.42;\n{body}\n'
        path = f't/{n}-fault-format-{name}'
        open(path + '.pl', 'w', encoding='utf-8').write(program)
        open(path + '.expected', 'w', encoding='utf-8').write(f'{before}fault: {message} at {path}.pl line {line + 3}.\nexit: 1\n')
        n += 1
    print(n - first_fault, 'fault tests,', first_fault, 'to', n - 1)
    n = first_refusal
    for name, why, body, at, message, nth in R:
        program = f'# kind: refused\n# {why}\nuse v5.42;\n{body}\n'
        path = f't/{n}-format-{name}'
        open(path + '.pl', 'w', encoding='utf-8').write(program)
        k = program.index('use v5.42;')
        for _ in range(nth):
            k = program.index(at, k + 1)
        line = program.count('\n', 0, k) + 1
        col = len(program[program.rfind('\n', 0, k) + 1:k]) + 1
        open(path + '.expected', 'w', encoding='utf-8').write(f'{path}.pl:{line}:{col}: {message}\nexit: 1\n')
        n += 1
    print(n - first_refusal, 'refusal tests,', first_refusal, 'to', n - 1)


write(int(sys.argv[1]), int(sys.argv[2]))
