#!/usr/bin/env python3
# Writes step 16a's refusal tests from a table written by hand: the program,
# the text the message points at (its column is counted here, from the
# program's own text), and the message. Nothing here asks the compiler.
# What perl does with each is in its comment, pasted from perl 5.42.
#
#     python3 docs/briefs/step16a-refusals.py 2620
import sys
T = []
def r(name, why, body, at, message, nth=1):
    T.append((name, why, body, at, message, nth))

DELIM = lambda w: f'{w} takes a bracket hard against it, and no other delimiter: {w}(...), {w}[...], {w}{{...}} or {w}<...> (D121)'

# ---- q, qq, qw (D121, D122)
r('q-slash', 'perl prints x.', 'say q/x/;', 'q/', DELIM('q'))
r('q-blank-before-the-bracket', 'perl prints x.', 'say q (x);', 'q (', DELIM('q'))
r('q-hash-delimiter', 'perl prints y: with no blank, # is the delimiter.', 'say q#y#;', 'q#', DELIM('q'))
r('qq-bang', 'perl prints x.', 'say qq!x!;', 'qq!', DELIM('qq'))
r('qw-slash', 'perl prints ab.', 'say qw/a b/;', 'qw/', DELIM('qw'))
r('q-never-ends', 'perl: Can\'t find string terminator ")" anywhere before EOF.', 'say q(abc;', 'q(', 'q(...) that never ends: it begins here')
r('qq-never-ends-nested', 'perl: Can\'t find string terminator "}" anywhere before EOF.', 'say qq{a{b};', 'qq{', 'qq{...} that never ends: it begins here')
r('qw-comma', 'perl warns: Possible attempt to separate words with commas.', 'say join "|", qw(a,b c);', ',b', 'a comma in qw(...): perl warns that it may be meant to separate the words, and keeps it in one')
r('qw-hash', 'perl warns: Possible attempt to put comments in qw() list.', 'say join "|", qw(a #b c);', '#b', "a '#' in qw(...): perl warns that it may be meant for a comment, and keeps it in a word")
r('qw-backslash', 'perl keeps it: a\\|b.', 'say join "|", qw(a\\ b);', '\\ b', 'a backslash in qw(...): perl keeps it, or takes it away before a bracket (T261); write the list in quotes')
r('qw-backslash-before-a-bracket', 'perl takes it away: a(b|c.', 'say join "|", qw(a\\(b c);', '\\(', 'a backslash in qw(...): perl keeps it, or takes it away before a bracket (T261); write the list in quotes')
r('qw-for-without-brackets', 'perl does not compile it: syntax error (T260).', 'for my $x qw(a b) { say $x }', 'qw(', "expected '(' after for my $x, found 'qw'")
r('qw-if-without-brackets', 'perl does not compile it: syntax error (T260).', 'if qw(a) { say 1 }', 'qw(', "expected '(' after if, found 'qw(a)'")
r('qw-for-one-value', 'perl gives the last word, and warns: Useless use of a constant ("a") in void context.', 'my $x = qw(a b);\nsay $x;', 'qw(', 'a list where one value is wanted: perl gives its last value, and warns of the others')
r('qq-index-past-the-end', 'perl ends the string at the first ")", and does not compile: Missing right curly or square bracket.', 'my @a = (1, 2);\nsay qq($a[1)]);', ')]', 'in a string an index is a whole number or a scalar variable (D91): take the index into a my first')
r('qq-code', 'perl runs the code: 1.', 'say qq(@{[ 1 ]});', '@{', '@{[ in a string takes a reference, and a reference in a string is not in the language yet (step 13d)')
r('qq-case-escape', 'perl prints AB: the case escapes are step 16d (D120).', 'my $x = "ab";\nsay qq(\\U$x);', '\\U', '\\U is not an escape in the language')
r('q-past-ascii-without-utf8', 'perl does not compile it: Use of non-ASCII character 0xC3 illegal (T73).', 'say q(é);', 'é', "a character past ASCII (U+00E9) needs 'use utf8;' on a line before it")
r('use-open-qw', 'perl takes it; one spelling of the pragma (D39).', "use open qw(:std :encoding(UTF-8));\nsay 1;", 'use open', "'use open' is written: use open ':std', ':encoding(UTF-8)';")
# ---- heredocs (D123)
r('heredoc-blank-after', 'perl prints x.', 'print << "EOT";\nx\nEOT', '<<', "a blank after '<<': a heredoc's terminator is a word hard against it, <<\"END\"")
r('heredoc-blank-after-squiggle', 'perl prints x.', 'print <<~ "EOT";\nx\nEOT', '<<', "a blank after '<<~': a heredoc's terminator is a word hard against it, <<~\"END\"")
r('heredoc-empty-terminator', 'perl reads to the first empty line: a, then x.', 'print <<"";\na\n\nsay "x";', '<<', "a heredoc's terminator is a word, a letter or '_' first: <<\"END\"")
r('heredoc-terminator-with-a-blank', 'perl prints a.', 'print <<"E O";\na\nE O', '<<', "a heredoc's terminator is a word between its quotes: <<\"END\"")
r('heredoc-two-on-a-line', 'perl prints a, then b.', 'print <<A, <<B;\na\nA\nb\nB', '<<B', 'a second heredoc on one line: write each on a line of its own')
r('heredoc-never-ends', 'perl: Can\'t find string terminator "EOT" anywhere before EOF.', 'print <<EOT;\nnever', '<<', 'a heredoc that never ends: no line is EOT alone')
r('heredoc-terminator-after-blanks', 'perl: Can\'t find string terminator "EOT" anywhere before EOF: without ~ the line is EOT alone.', 'print <<EOT;\na\n  EOT', '<<', 'a heredoc that never ends: no line is EOT alone')
r('heredoc-indent-short', "perl dies: Indentation on line 2 of here-doc doesn't match delimiter (T263).", 'print <<~EOT;\n    a\n  b\n    EOT', '  b', 'a line of a <<~ heredoc that does not begin with the blanks before its terminator: perl dies (T263)')
r('heredoc-indent-tab', "perl dies: Indentation on line 1 of here-doc doesn't match delimiter (T263).", 'print <<~EOT;\n\ta\n    EOT', '\ta', 'a line of a <<~ heredoc that does not begin with the blanks before its terminator: perl dies (T263)')
r('heredoc-indent-blank-line', "perl dies: Indentation on line 2 of here-doc doesn't match delimiter.", 'print <<~EOT;\n    a\n  \n    EOT', '  \n', 'a line of a <<~ heredoc that does not begin with the blanks before its terminator: perl dies (T263)')
r('heredoc-string-past-its-line', 'perl does not compile it: Can\'t find string terminator \'"\' anywhere before EOF (T264).', 'say <<EOT . "a\nb";\nc\nEOT', '<<', 'this goes on past the end of the line a heredoc stands on: perl reads the body after it, or does not find it (T264)')
r('heredoc-qw-past-its-line', 'perl does not compile it: Can\'t find string terminator ")" anywhere before EOF.', 'my @l = (<<EOT, qw(a\nb));\nc\nEOT\nsay scalar(@l);', '<<', 'this goes on past the end of the line a heredoc stands on: perl reads the body after it, or does not find it (T264)')
r('heredoc-backslash-at-a-line-end', 'perl takes the backslash away: a and b on two lines. A backslash before a new line is refused everywhere (D43).', 'print <<"EOT";\na\\\nb\nEOT', '\\\n', 'a backslash before the end of a line is not in the language')
r('heredoc-variable-runs-on', 'perl reads the index across the line as code: 1.', 'my @a = (1);\nprint <<"EOT";\n$a[\n0]\nEOT', '\n0]', 'in a string an index is a whole number or a scalar variable (D91): take the index into a my first')
r('qq-backslash-before-its-bracket', 'perl takes the backslash away first: Y, the element (T278).', 'my $x = "X";\nmy @x = ("Y");\nsay qq[$x\\[0\\]];', '\\[0', "a backslash before '[' in a qq with that bracket: perl takes it away before it reads the variables, so that what follows can go on with one (T278); write the string with other brackets")
r('qq-backslash-before-its-closing-bracket', 'perl prints a)b: no variable here, and one rule for the bracket.', 'say qq(a\\)b);', '\\)', "a backslash before ')' in a qq with that bracket: perl takes it away before it reads the variables, so that what follows can go on with one (T278); write the string with other brackets")
r('heredoc-first-of-arguments-over-lines', 'perl takes the next line into the body, and does not compile the rest: Global symbol "@a" requires explicit package name (T284).', 'my @a = (<<A,\n"x");\nbody\nA\nsay scalar(@a);', 'say', 'say is a statement, and has no value')
r('heredoc-after-a-value', 'perl takes $x for a file handle: Can\'t use string ("1") as a symbol ref. Here << after a value is the left shift, not in the language.', 'my $x = 1;\nsay $x <<EOT;\nEOT', '<<', "'<<' is not in the language yet")


def write(first):
    n = first
    for name, why, body, at, message, nth in T:
        program = f'# kind: refused\n# {why}\nuse v5.42;\n{body}\n'
        path = f't/{n}-quote-{name}'
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
