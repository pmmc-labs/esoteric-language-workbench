#!/usr/bin/env python3
# Writes step 16c's fault and refusal tests from tables written by hand,
# as docs/briefs/step16b-tests.py does. Nothing here asks the compiler.
# What perl does with each is in its comment, pasted from perl 5.42.
#
#     python3 docs/briefs/step16c-tests.py 2820 2840
import sys

F = []
R = []


def f(name, why, body, before, message, line):
    F.append((name, why, body, before, message, line))


def r(name, why, body, at, message, nth=1):
    R.append((name, why, body, at, message, nth))


U = 'use utf8;\nuse open ":std", ":encoding(UTF-8)";\n'

# ---- faults
f('ucfirst-past-ascii', 'perl gives the capital E with an acute, by its tables (titlecase).', U + 'say ucfirst("aé");\nsay ucfirst("éa");', 'Aé\n', 'ucfirst of a character past ASCII', 4)
f('lcfirst-past-ascii', 'perl gives a small e with an acute, then a.', U + 'say lcfirst("Éa");', '', 'lcfirst of a character past ASCII', 3)
f('chomp-undef', 'perl warns: Use of uninitialized value $s in scalar chomp (T272).', 'my $s;\nchomp($s);\nsay "not reached";', '', 'undef where a string is wanted', 2)
f('chop-undef', 'perl warns: Use of uninitialized value $s in scalar chop.', 'my $s;\nchop $s;', '', 'undef where a string is wanted', 2)
f('chop-whole-float', 'perl makes the string 1e+15, and chops it to 1e+1 (D36).', 'my $x = 1e15;\nchop($x);\nsay $x;', '', 'a whole float this size prints two ways in perl (add 0 to print the integer)', 2)
f('rindex-past-the-ints', 'perl gives -1 or 0 by whether the string is UTF-8 inside (T281).', 'say rindex("abc", "a", 9223372036854775806);\nsay rindex("abc", "a", 9223372036854775807);', '0\n', 'an rindex position this far past the end has two answers in perl', 2)
f('rindex-of-undef', 'perl warns: Use of uninitialized value in rindex.', 'my $u;\nsay rindex($u, "a");', '', 'undef where a string is wanted', 2)
f('rindex-position-not-a-number', 'perl warns: Argument "x" isn\'t numeric in rindex.', 'say rindex("abc", "a", "x");', '', 'not a numeric string', 1)
f('chomp-last-in-a-sub', 'perl gives the count chomp took: 1. Here chomp is no value, a sub\'s either (D130).', 'sub f($s) { chomp $s }\nsay "before";\nsay f("a\\n");', 'before\n', 'f has no value: it does not end in a return or an expression', 1)

# ---- refusals
ONE = lambda w: f'{w} takes one scalar variable here, {w}($x): its value, an array, a hash, an element and $_ are not in the language (D130)'
VALUE = lambda w, what: f'{w} is a statement here, and has no value: perl gives {what} (D130)'
r('chomp-as-a-value', 'perl gives how many characters it took, 1, to $n.', 'my $s = "a\\n";\nmy $n = chomp($s);', 'chomp', VALUE('chomp', 'how many characters it took'))
r('chomp-tested', 'perl tests the count: y.', 'my $s = "a\\n";\nif (chomp $s) { say "y" }', 'chomp', VALUE('chomp', 'how many characters it took'))
r('chop-as-a-value', 'perl gives the character it took: b.', 'my $s = "ab";\nsay chop($s);', 'chop', VALUE('chop', 'the character it took'))
r('chomp-of-an-array', 'perl chomps each element.', 'my @a = ("a\\n");\nchomp(@a);', '@a', ONE('chomp'), 2)
r('chomp-of-an-element', 'perl chomps the element.', 'my @a = ("a\\n");\nchomp $a[0];', '$a', ONE('chomp'))
r('chomp-of-a-hash-element', 'perl chomps the element.', 'my %h = (k => "v\\n");\nchomp $h{k};', '$h', ONE('chomp'))
r('chomp-of-a-my', 'perl declares $t, assigns it and chomps it.', 'my $s = "ab\\n";\nchomp(my $t = $s);', 'my $t', ONE('chomp'))
r('chomp-of-it', 'perl chomps $_, which is undef here, and warns.', 'chomp;', ';', ONE('chomp'), 2)
r('chomp-for', 'perl chomps each of the list through $_.', 'my ($x, $y) = ("a\\n", "b\\n");\nchomp for $x, $y;', 'for', ONE('chomp'))
r('chomp-two', 'perl chomps both.', 'my ($x, $y) = ("a\\n", "b\\n");\nchomp($x, $y);', '$x, $y)', ONE('chomp'), 2)
r('chop-of-a-loop-variable', 'perl chops the array\'s own elements: a c (T9).', 'my @a = ("ab", "cd");\nfor my $x (@a) { chop $x }', 'chop $x', "$x is its loop's variable, and read-only: in perl, changing it changes the list's own element; take the value into a my")
r('ucfirst-no-argument', 'perl takes $_.', 'say ucfirst;', 'ucfirst', 'ucfirst needs an argument')
r('rindex-no-brackets', 'perl takes it: 1.', 'say rindex "abc", "b";', 'rindex', 'rindex needs brackets round its arguments: rindex(...)')
r('rindex-one-argument', 'perl does not compile it: Not enough arguments for rindex.', 'say rindex("abc");', 'rindex', 'rindex takes 2 to 3 arguments, and here are 1')
r('lcfirst-minus', 'perl warns that it is ambiguous.', 'say lcfirst - 5;', '-', "lcfirst -: perl warns that this is ambiguous: write lcfirst(-...)")


def write(first_fault, first_refusal):
    n = first_fault
    for name, why, body, before, message, line in F:
        program = f'# kind: fault\n# {why}\nuse v5.42;\n{body}\n'
        path = f't/{n}-fault-{name}'
        open(path + '.pl', 'w', encoding='utf-8').write(program)
        open(path + '.expected', 'w', encoding='utf-8').write(f'{before}fault: {message} at {path}.pl line {line + 3}.\nexit: 1\n')
        n += 1
    print(n - first_fault, 'fault tests,', first_fault, 'to', n - 1)
    n = first_refusal
    for name, why, body, at, message, nth in R:
        program = f'# kind: refused\n# {why}\nuse v5.42;\n{body}\n'
        path = f't/{n}-{name}'
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
