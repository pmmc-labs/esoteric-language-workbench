#!/usr/bin/env python3
"""t/2600 to t/2603: q, qq, qw and heredocs (step 16a; D121 to D123).

The definition, which is all this file knows of the language beyond the
double-quoted strings of t/models/str.py and t/models/interp.py:

  q(...)     the characters between the brackets, as they are, but that a
             backslash before a backslash or before either bracket is
             taken away; brackets of the kind nest, and a backslash takes
             the character after it with it as perl finds the end
  qq(...)    a double-quoted string, its escapes and its variables those
             of "...", the bracket for the quote; a backslash before
             that bracket is refused (T278)
  qw(...)    the words between blanks: a bracketed list of strings
  heredoc    <<"E" and <<E: the lines after the heredoc's line, to a line
             that is E alone, as a double-quoted string; <<'E': every
             character as it is; with ~, the blanks before the last E
             taken off each line

with [ ], { } and < > for ( ). The model writes a body at random from
pieces that are safe on their own (a word, a blank, a nested pair of the
delimiter's kind, an escape, a variable followed by a blank), and works
out what it stands for; perl is the second derivation (t/checks.py
oracle).

2600 is q, 2601 qq, 2602 qw, 2603 heredocs.

Every command that writes a file, one a line (t/checks.py runs them all):

    python3 t/models/quote.py --program 2600 > t/2600-q.pl
    python3 t/models/quote.py 2600 > t/2600-q.expected
    python3 t/models/quote.py --program 2601 > t/2601-qq.pl
    python3 t/models/quote.py 2601 > t/2601-qq.expected
    python3 t/models/quote.py --program 2602 > t/2602-qw.pl
    python3 t/models/quote.py 2602 > t/2602-qw.expected
    python3 t/models/quote.py --program 2603 > t/2603-heredocs.pl
    python3 t/models/quote.py 2603 > t/2603-heredocs.expected
"""

import random
import sys

PAIRS = [('(', ')'), ('[', ']'), ('{', '}'), ('<', '>')]
WORDS = ['a', 'bc', 'X', '9', '-', '+', '.', ',', ';', ':', '=', '!', '?', '/', '"', "'", '|', '^', '*', '&', '%', '~']
DECLS = 'my $x = "X"; my $n = 42; my @a = (1, 2); my @e = (); my %h = (k => "v");\n'


def q_body(rnd, o, c, depth=0):
    """A q body, and what it stands for."""
    src, val = [], []
    for _ in range(rnd.randint(0, 6)):
        k = rnd.randrange(10)
        if k < 4:
            w = rnd.choice(WORDS + [p for pr in PAIRS if pr != (o, c) for p in pr])
            src.append(w); val.append(w)
        elif k == 4:
            src.append(' '); val.append(' ')
        elif k == 5 and depth < 2:
            s, v = q_body(rnd, o, c, depth + 1)
            src.append(o + s + c); val.append(o + v + c)
        elif k == 6:
            ch = rnd.choice(['\\', o, c])
            src.append('\\' + ch); val.append(ch)
        elif k == 7:
            ch = rnd.choice(['n', 't', 'x', '$', 'q', '"'])
            src.append('\\' + ch); val.append('\\' + ch)
        elif k == 8:
            src.append('$x @a'); val.append('$x @a')
        else:
            src.append('\\\\'); val.append('\\')
    return ''.join(src), ''.join(val)


ESC = [('\\n', '\n'), ('\\t', '\t'), ('\\\\', '\\'), ('\\"', '"'), ('\\$', '$'), ('\\@', '@'),
       ('\\x41', 'A'), ('\\x{263A}', '☺'), ('\\101', 'A'), ('\\N{U+42}', 'B'), ('\\e', '\x1b'), ('\\0', '\0')]
VARS = [('$x', 'X'), ('${x}', 'X'), ('$n', '42'), ('@a', '1 2'), ('@{a}', '1 2'), ('@e', ''), ('$a[1]', '2'),
        ('$a[-2]', '1'), ('@a[0, 1]', '1 2'), ('$#a', '1'), ('$h{k}', 'v')]


def qq_body(rnd, o, c, depth=0, quote=None):
    """A qq body (or a double-quoted heredoc line, quote None and o None),
    and what it stands for."""
    src, val = [], []
    for _ in range(rnd.randint(0, 6)):
        k = rnd.randrange(10)
        if k < 3:
            pool = [w for w in WORDS if w not in ('%',)] + [p for pr in PAIRS if pr != (o, c) for p in pr]
            if o is None:
                pool = [w for w in pool if w not in ('<',)]
            w = rnd.choice(pool)
            src.append(w); val.append(w)
        elif k == 3:
            src.append(' '); val.append(' ')
        elif k == 4 and depth < 2 and o is not None:
            s, v = qq_body(rnd, o, c, depth + 1)
            src.append(o + s + c); val.append(o + v + c)
        elif k == 5 and o is not None:
            # A backslash before the delimiter's own bracket is refused in
            # a qq (T278); before another kind it is that bracket.
            ch = rnd.choice([p for pr in PAIRS if pr != (o, c) for p in pr])
            src.append('\\' + ch); val.append(ch)
        elif k in (6, 7):
            s, v = rnd.choice(ESC)
            src.append(s); val.append(v)
        else:
            s, v = rnd.choice(VARS)
            # A blank after it, so that nothing goes on with the name.
            src.append(s + ' '); val.append(v + ' ')
    return ''.join(src), ''.join(val)


def perl_quote(v):
    """v as a single-quoted string of the language, for the program's
    own comparisons."""
    return "'" + v.replace('\\', '\\\\').replace("'", "\\'") + "'"


def case_q(rnd):
    lines, out = [], []
    for o, c in PAIRS:
        for _ in range(12):
            s, v = q_body(rnd, o, c)
            lines.append(f'say "[", q{o}{s}{c}, "]";')
            out.append(f'[{v}]')
    lines.append('say length q(), length q{}, length q[ ], q<a> . q(b);')
    out.append('001ab')
    return lines, out


def case_qq(rnd):
    lines, out = [], []
    for o, c in PAIRS:
        for _ in range(14):
            s, v = qq_body(rnd, o, c)
            lines.append(f'say "[", qq{o}{s}{c}, "]";')
            out.append(f'[{v}]')
    lines.append('say length qq(), qq{$x}, qq($x) . q($x);')
    out.append('0XX$x')
    return lines, out


def case_qw(rnd):
    lines, out = [], []
    chars = [ch for ch in 'abcXYZ019_-+.:;=!?/"\'|^*&~$@%' ]
    for o, c in PAIRS:
        for _ in range(10):
            words = [''.join(rnd.choice(chars) for _ in range(rnd.randint(1, 4))) for _ in range(rnd.randint(0, 5))]
            blanks = lambda: rnd.choice([' ', '  ', '\t', '\n  ', ' \n'])
            body = (blanks() if rnd.random() < 0.5 else '') + ''.join(w + blanks() for w in words)
            if words and rnd.random() < 0.5:
                body = body.rstrip(' \t\n')
            lines.append(f'{{ my @w = qw{o}{body}{c}; say scalar(@w), ":", join("|", @w); }}')
            out.append(f'{len(words)}:' + '|'.join(words))
    # A qw is a bracketed list (D122): sliced, repeated, assigned.
    lines += [
        'say qw(a b c)[1], qw<a b c>[-1], join("", (qw(a b c))[0, 2]);',
        '{ my @l = qw(a b) x 2; say "@l"; }',
        '{ my ($p, $q, @r) = qw(p q r s); say $p, $q, "@r"; }',
        '{ my $one = qw(only); say $one; }',
        '{ my @l = qw(a) x 3; say scalar(@l), "@l"; }',
        'say join(",", map { uc($_) } qw(x y)), " ", join(",", sort { $b cmp $a } qw(m z a));',
        'for my $w (qw(i j)) { say $w }',
        'say "a" . qw(b) . "c";',
    ]
    out += ['bcac', 'a b a b', 'pqr s', 'only', '3a a a', 'X,Y z,m,a', 'i', 'j', 'abc']
    return lines, out


def heredoc(rnd, kind, squiggle):
    """The program's lines for one heredoc, and what it stands for."""
    word = rnd.choice(['END', 'EOT', 'TEXT', 'E_2'])
    head = {'"': f'<<{"~" if squiggle else ""}"{word}"', "'": f"<<{'~' if squiggle else ''}'{word}'",
            '': f'<<{"~" if squiggle else ""}{word}'}[kind]
    indent = rnd.choice(['  ', '    ', '\t']) if squiggle else ''
    body, val = [], []
    for _ in range(rnd.randint(0, 4)):
        if rnd.random() < 0.15:
            body.append(''); val.append('')
            continue
        extra = rnd.choice(['', ' ', '  ']) if squiggle else rnd.choice(['', ' '])
        if kind == "'":
            s = ''.join(rnd.choice(['a', ' ', '\\', "'", '"', '$x', '@a', '\\n', '#', 'q(', '}']) for _ in range(rnd.randint(0, 6)))
            v = s
        else:
            s, v = qq_body(rnd, None, None)
            v = v.replace('\n', '\\n') if False else v
        body.append(indent + extra + s)
        val.append(extra + s if kind == "'" else extra + v)
    text = ''.join(v + '\n' for v in val)
    return head, body + [indent + word], text


def case_heredocs(rnd):
    lines, out = [], []
    for kind in ('"', "'", ''):
        for squiggle in (False, True):
            for _ in range(5):
                head, rest, text = heredoc(rnd, kind, squiggle)
                lines.append(f'print "[", {head}, "]\\n";')
                lines += rest
                out.append(f'[{text}]')
    # A heredoc is a value where it stands (D123).
    lines += ['my $s = lc <<END . "tail\\n";', 'ABC', 'END', 'print $s;',
              'print(<<END);', 'in brackets', 'END',
              'say length <<\'END\'; # a comment after it', '12345', 'END',
              'say "a', 'b" . <<END;', 'c', 'END']
    out += ['abc\ntail', 'in brackets', '6', 'a\nbc\n']
    return lines, out


CASES = {2600: case_q, 2601: case_qq, 2602: case_qw, 2603: case_heredocs}


def main(argv):
    program = argv[0] == '--program'
    n = int(argv[-1])
    lines, out = CASES[n](random.Random(n))
    if program:
        sys.stdout.write(f'# t/models/quote.py {n}\nuse v5.42;\nuse utf8;\nuse open \':std\', \':encoding(UTF-8)\';\n' + DECLS + '\n'.join(lines) + '\n')
    else:
        sys.stdout.write('\n'.join(out) + '\n')


if __name__ == '__main__':
    main(sys.argv[1:])
