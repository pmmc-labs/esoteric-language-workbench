#!/usr/bin/env python3
# Writes step 15's refusal tests from a table written by hand: the program,
# the text the message points at (its column is counted here, from the
# program's own text), and the message. Nothing here asks the compiler.
# What perl does with each is in its comment, pasted from perl 5.42.
#
#     python3 docs/briefs/step15-refusals.py 3100
import sys
T = []
def r(name, why, body, at, message, nth=1):
    T.append((name, why, body, at, message, nth))

TESTED = 'a die that is tested: perl warns of a precedence problem, and a die is never worth anything'
LEFT = lambda op: f"a die on the left of '{op}': perl warns of a precedence problem, and a die is never worth anything"
LINES = 'a {} in a statement, a test or a header over more than one line: perl names a line of its own choosing there, and the message would carry it; put it on one line, or end the message in a newline'
LOOP = "a {} in the test of a while or an until: perl names the line of the last statement the loop's block ran, and the message would carry it; end the message in a newline, or work the test out in the block"
DIRECTIVE = "a comment that begins its line '# line' and a number is a line directive, to perl, which changes the line and the file a die names: reword it"

# ---- a die tested, or first (D146, T303)
r('die-left-of-a-dot', 'perl warns: Possible precedence issue with control flow operator (die).', 'my $x = die("x") . "y";', 'die', LEFT('.'))
r('die-left-of-or-in-brackets', 'perl is silent here, and dies x; refused all the same (D146).', 'my $x = (die "x") || 1;', 'die', LEFT('||'))
r('die-left-of-a-plus', 'perl warns of a precedence problem.', 'my $x = die("x") + 1;', 'die', LEFT('+'))
r('die-tested-by-if', 'perl warns of a precedence problem.', 'if (die "u") { say 1; }', 'die', TESTED)
r('die-tested-by-a-modifier', 'perl warns of a precedence problem.', 'say 1 if die "q";', 'die', TESTED)
r('die-tested-by-a-ternary', 'perl warns of a precedence problem.', 'my $x = die("x") ? 1 : 2;', 'die', TESTED)
r('die-tested-by-until', 'perl is silent here, and dies; refused all the same (D146).', 'until (die "x\\n") { say 1; }', 'die', TESTED)
r('die-tested-by-elsif', 'perl warns of a precedence problem.', 'my $x = 0;\nif ($x) { say 1; } elsif (die "e") { say 2; }', 'die', TESTED)
r('die-tested-by-a-for', 'perl warns of a precedence problem.', 'for (my $i = 0; die "f\\n"; $i++) { say $i; }', 'die', TESTED)
r('or-die-as-a-statement', 'perl dies zero (D146: die ... unless ...).', 'my $x = 0;\n$x or die "zero\\n";', 'or', "'or die' after a statement: a statement is not joined by a word operator here (D56); write die ... unless ...;")
r('and-die-as-a-statement', 'perl dies one.', 'my $x = 1;\n$x and die "one\\n";', 'and', "'and die' after a statement: a statement is not joined by a word operator here (D56); write die ... if ...;")
r('die-then-or', 'perl warns of a precedence problem, and dies x.', 'die "x" or say 1;', 'or', "'or' in a list of arguments takes the whole list for its left side, to perl: bracket what it joins")
# ---- a die whose line perl chooses (D150, T316, T317)
r('die-in-a-statement-over-two-lines', 'perl: a at FILE line 5, the second line (T317).', 'my %h = (k => 1);\n$h{k} =\n  die "a";', 'die', LINES.format('die'))
r('die-list-over-two-lines', 'perl: ab at FILE line 2; refused, since the message carries a line.', 'die "a",\n  "b";', 'die', LINES.format('die'))
r('die-in-a-test-over-two-lines', 'perl: the line of the if; refused all the same.', 'my $x;\nif ($x\n  // die "u") { say 1; }', 'die', LINES.format('die'))
r('die-in-a-header-over-two-lines', 'perl: the line of the for; refused all the same.', 'my $x;\nfor my $i (1,\n  $x // die "u") { say $i; }', 'die', LINES.format('die'))
r('die-in-a-default-over-two-lines', 'perl: the parameter\'s line.', 'sub f($y =\n  die "d") { return $y; }\nsay f(1);', 'die', LINES.format('die'))
r('die-in-a-return-over-two-lines', 'perl: r at FILE line 5 (T317).', 'my %h = (k => 1);\nsub g() {\n  return $h{k} +\n    die "r";\n}\nsay g();', 'die', LINES.format('die'))
r('die-in-a-while-test', 'perl: the line of the last statement the block ran (T316).', 'my $i = 0;\nwhile ($i < 2 || die "w") { $i++; }', 'die', LOOP.format('die'))
r('die-in-an-until-test', 'perl: u at the line of the if (T316).', 'my $j = 0;\nuntil ($j >= 1 && die "u") { $j++; }', 'die', LOOP.format('die'))
r('die-in-a-map-in-a-statement-over-lines', 'perl: the line of the block\'s statement, 2; refused, the block being one statement over two lines.', 'my @a = map { $_ == 2 ?\n  die("m") : $_ } (1, 2);', 'die', LINES.format('die'))
# ---- try and catch (D143, T53)
r('try-with-no-catch', 'perl does not compile it: syntax error.', 'try { die "x\\n" } say 1;', 'say', 'a try has a catch after its block: perl refuses it without one')
r('catch-with-no-variable', 'perl does not compile it: catch block requires a (VAR) (T53).', 'try { die "x\\n" } catch { say "c"; }', '{ say', 'catch is followed by its variable in brackets, catch ($e): perl refuses it without (T53)')
r('catch-an-array', 'perl does not compile it: syntax error.', 'try { die "x\\n" } catch (@e) { say "c"; }', '@e', "the variable of a catch is a scalar, catch ($e), found '@e'")
r('catch-dollar-a', 'perl takes it; $a is the sort\'s (D55).', 'try { die "x\\n" } catch ($a) { say "c"; }', '$a', '$a is not a name a program may declare: $a and $b are the two values a sort gives its block')
r('catch-dollar-underscore', 'perl does not compile it: Can\'t use global $_ in "my".', 'try { die "x\\n" } catch ($_) { say "c"; }', '$_', '$_ is not a name a program may declare: it is what a for, a map or a grep gives its block')
r('two-catches', 'perl does not compile it: syntax error.', 'try { die "x\\n" } catch ($e) { say 1; } catch ($f) { say 2; }', 'catch ($f', 'a second catch: perl takes one')
r('finally', 'perl warns: try/catch/finally is experimental (T313, D144).', 'try { die "x\\n" } catch ($e) { say "c"; } finally { say "f"; }', 'finally', 'finally: perl 5.42 warns that it is experimental, and it is not in the language (D144)')
r('defer', 'perl does not compile it: syntax error (T313, D144).', '{ defer { say "d"; } say "b"; }', 'defer', "'defer' is not in the language")
r('try-as-a-value', 'perl does not compile it: syntax error.', 'my $x = try { 1 } catch ($e) { 2 };', 'try', 'try is a statement, not a value: perl does not compile it here')
r('catch-alone', 'perl does not compile it: syntax error.', 'catch ($e) { say 1; }', 'catch', 'catch without a try before it')
r('label-on-a-try', 'perl takes it; a label is on a loop (D61).', 'L: try { die "x\\n" } catch ($e) { say 1; }', 'try', 'a label is on a loop: after L: comes while, until or for')
r('semicolon-after-a-try', 'perl takes it; there is no empty statement.', 'try { die "x\\n" } catch ($e) { say 1; };', ';\n', "expected a statement, found ';'", 2)
r('eval', 'perl takes it; eval is cut (D20).', 'eval { die "x\\n" };', 'eval', "'eval' is not in the language")
# ---- ... (D145, T315)
r('yada-with-a-modifier', 'perl does not compile it: syntax error (T315).', '... if 1;', 'if', "'...' is a statement alone: perl does not compile anything after it but ';'")
r('yada-as-a-value', 'perl does not compile it: syntax error (T315).', 'my $x = ...;', '...', "'...' is a statement alone, which dies: perl does not compile it anywhere else")
r('yada-after-a-value', 'perl takes it for its other range: a flip-flop.', 'my $x = 1 ... 2;', '...', "'...' is not in the language yet")
# ---- a line directive (D147, T74, T311)
r('line-directive', 'perl: x at other.pl line 100 (T74).', '# line 100 "other.pl"\ndie "x";', '# line', DIRECTIVE)
r('line-directive-hard-against', 'perl: x at FILE line 100 (T311).', '#line 100\ndie "x";', '#line', DIRECTIVE)
r('line-directive-zero', 'perl: x. and no place at all (T311).', '#\tline 0\ndie "x";', '#\t', DIRECTIVE)
# ---- warn and stderr (15b)
r('warn-in-a-while-test', 'perl: the line of the last statement the block ran (T316).', 'my $i = 0;\nwhile ($i++ < 2 || warn "w") { say $i; last; }', 'warn', LOOP.format('warn'))
r('warn-over-two-lines', 'perl names a line of its own choosing (T317).', 'my %h = (k => 1);\nmy $x = $h{k} +\n  warn "w";', 'warn', LINES.format('warn'))
r('say-stderr-of-nothing', 'perl prints $_, which is not in the language here.', 'say STDERR;', ';\n', 'say STDERR with nothing to print: perl prints $_', 2)
r('say-stderr-in-brackets', 'perl prints xy: the brackets are not the whole list (T320).', 'say STDERR ("x"), "y";', '("x")', 'say STDERR (...): write the list without brackets of its own, say STDERR ...;')
r('print-stdout', 'perl prints x; STDERR is the one handle.', 'print STDOUT "x\n";', 'STDOUT', "expected a value, found 'STDOUT'")
r('say-stderr-in-braces', 'perl prints x; the braces are not in the language.', 'say {STDERR} "x";', '{', "'{' first after say: perl takes it for a block that gives a file handle; write +{ ... } for a new hash")
# ---- what is in a try's blocks is checked as anywhere (closed by the breakages)
r('value-alone-in-a-try', 'perl warns: Useless use of addition in void context.', 'my $x = 1;\ntry { $x + 1; } catch ($e) { say "c"; }', '$x + 1', 'this statement only has a value, and nothing is done with it: perl warns that it is useless')
r('value-alone-in-a-catch', 'perl warns: Useless use of a constant in void context.', 'try { die "x\\n" } catch ($e) { "c"; }', '"c"', 'this statement only has a value, and nothing is done with it: perl warns that it is useless')
r('row-of-dots-and-a-sub-that-changes-in-a-try', 'perl reads $x after ch has run: bc (D69).', 'my $x = "a";\nsub ch() { try { $x = "b"; } catch ($e) { } return "c"; }\nsay $x . ch();', 'ch();', 'a later piece of a concatenation calls ch, which can change $x, which an earlier piece reads: perl joins the pieces as one operation and reads each late; make the call a statement of its own')

def write(first):
    n = first
    for name, why, body, at, message, nth in T:
        program = f'# kind: refused\n# {why}\nuse v5.42;\n{body}\n'
        path = f't/{n}-try-{name}'
        open(path + '.pl', 'w', encoding='utf-8').write(program)
        k = program.index('use v5.42;')
        for _ in range(nth):
            k = program.index(at, k + 1)
        line = program.count('\n', 0, k) + 1
        col = len(program[program.rfind('\n', 0, k) + 1:k]) + 1
        open(path + '.expected', 'w', encoding='utf-8').write(f'{path}.pl:{line}:{col}: {message}\nexit: 1\n')
        n += 1
    print(n - first, 'tests,', first, 'to', n - 1)

write(int(sys.argv[1]))
