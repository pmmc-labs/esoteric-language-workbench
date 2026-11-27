#!/usr/bin/env python3
"""t/2800 and t/2801: ucfirst, lcfirst, rindex, chomp and chop (step 16c;
D129 to D131).

The definition, which is all this file knows of them:

  ucfirst S, lcfirst S   S made a string as `.` makes one, its first
                         character changed if it is an ASCII letter
  rindex(S, T)           where T last begins in S, or -1
  rindex(S, T, P)        the same, T ending at or before P + length(T),
                         which is first moved into the string: from 0 to
                         the length of S. So a P below zero finds only
                         the empty T, at 0 (T281)
  chomp($x);             a Str less one newline at its end; any other
                         value as it is (T279)
  chop($x);              the value made a string, less its last character

Positions and lengths count characters. perl is the second derivation
(t/checks.py oracle).

2800 is ucfirst, lcfirst and rindex; 2801 chomp and chop.

Every command that writes a file, one a line (t/checks.py runs them all):

    python3 t/models/strfn.py --program 2800 > t/2800-ucfirst-lcfirst-rindex.pl
    python3 t/models/strfn.py 2800 > t/2800-ucfirst-lcfirst-rindex.expected
    python3 t/models/strfn.py --program 2801 > t/2801-chomp-chop.pl
    python3 t/models/strfn.py 2801 > t/2801-chomp-chop.expected
"""

import random
import sys

ALPHA = 'abAB é☺\n-1'


def lit(s):
    out = ''
    for ch in s:
        out += {'\n': '\\n', '\r': '\\r', '"': '\\"', '\\': '\\\\', '$': '\\$', '@': '\\@'}.get(ch, ch)
    return '"' + out + '"'


def ucfirst(s):
    return s[:1].upper() + s[1:] if s[:1].isascii() else s


def lcfirst(s):
    return s[:1].lower() + s[1:] if s[:1].isascii() else s


def rindex(s, t, p=None):
    end = len(s) if p is None else max(0, min(len(s), p + len(t)))
    for k in range(end - len(t), -1, -1):
        if s[k:k + len(t)] == t:
            return k
    return -1


def case_first(rnd):
    lines, out = [], []
    for s in ['abc', 'Abc', 'ABC', '', 'z', 'Z', '1ab', ' ab', 'aé☺', '-x', '_y']:
        lines.append(f'say "[", ucfirst({lit(s)}), "|", lcfirst({lit(s)}), "|", ucfirst {lit(s)} . "+", "]";')
        out.append(f'[{ucfirst(s)}|{lcfirst(s)}|{ucfirst(s + "+")}]')
    lines.append('say ucfirst(5), lcfirst(1.5), ucfirst(true), "[", lcfirst(false), "]";')
    out.append('51.51[]')
    lines.append('{ my $w = "word"; say ucfirst lc uc $w; }')
    out.append('Word')
    for _ in range(60):
        s = ''.join(rnd.choice('abcab é☺') for _ in range(rnd.randint(0, 8)))
        t = ''.join(rnd.choice('ab é') for _ in range(rnd.randint(0, 2)))
        if rnd.random() < 0.3:
            lines.append(f'say rindex({lit(s)}, {lit(t)});')
            out.append(str(rindex(s, t)))
        else:
            p = rnd.randint(-4, len(s) + 3)
            lines.append(f'say rindex({lit(s)}, {lit(t)}, {p if p >= 0 else f"({p})"});')
            out.append(str(rindex(s, t, p)))
    # A position below zero finds only the empty piece (T281).
    lines.append('say rindex("abc", "a", -1), rindex("abc", "abc", -3), rindex("abc", "", -1), rindex("aaa", "a", 0), rindex("abc", "ab", 0);')
    out.append(f'{rindex("abc", "a", -1)}{rindex("abc", "abc", -3)}{rindex("abc", "", -1)}{rindex("aaa", "a", 0)}{rindex("abc", "ab", 0)}')
    lines.append('say rindex("abcabc", "c", 4.9), rindex("abc", "", 9223372036854775807 - 1), rindex(123123, 2), rindex("x1.5", 1.5);')
    out.append(f'{rindex("abcabc", "c", 4)}{rindex("abc", "", 10)}{rindex("123123", "2")}{rindex("x1.5", "1.5")}')
    return lines, out


def case_chomp(rnd):
    lines, out = [], []
    for s in ['ab\n', 'ab\n\n', 'ab', '', '\n', 'a\r\n', 'é\n', '☺', 'x\ny', '\n\n']:
        lines.append(f'{{ my $s = {lit(s)}; chomp($s); my $t = {lit(s)}; chop $t; say "[$s|$t]"; }}')
        c = s[:-1] if s.endswith('\n') else s
        out.append(f'[{c}|{s[:-1]}]')
    # A number chomped is the number (T279); chopped, its string less one.
    lines += [
        '{ my $x = 1 / 3; chomp($x); say $x * 3; }',
        '{ my $x = 0.1 + 0.2; chomp $x; say $x - 0.3; }',
        '{ my $n = 42; chomp($n); say $n + 1; }',
        '{ my $t = true; chomp($t); say $t + 1; }',
        '{ my $x = 1.5; chop($x); say $x, "|", $x + 1; }',
        '{ my $n = 42; chop $n; say $n; }',
        '{ my $s = "abc"; chop $s; chop $s; chop $s; chop $s; say "[$s]"; }',
        '{ my $s = "line\\n"; chomp $s if 1; say "[$s]"; }',
        '{ my $s = "a\\n"; chomp $s unless 0; say "[$s]"; }',
        '{ my @l = ("x\\n", "y\\n"); my @r; for my $e (@l) { my $c = $e; chomp $c; push @r, $c; } say join("|", @r); }',
        'sub trimmed($line) { chomp $line; return $line } say "[", trimmed("in a sub\\n"), "]";',
        '{ my $s = "abc\\n"; chomp($s); chop($s); say length $s, $s; }',
    ]
    out += ['1', '5.55111512312578e-17', '43', '2', '1.|2', '4', '[]', '[line]', '[a]', 'x|y', '[in a sub]', '2ab']
    return lines, out


CASES = {2800: case_first, 2801: case_chomp}


def main(argv):
    program = argv[0] == '--program'
    n = int(argv[-1])
    lines, out = CASES[n](random.Random(n))
    if program:
        sys.stdout.write(f'# t/models/strfn.py {n}\nuse v5.42;\nuse utf8;\nuse open \':std\', \':encoding(UTF-8)\';\n' + '\n'.join(lines) + '\n')
    else:
        sys.stdout.write('\n'.join(out) + '\n')


if __name__ == '__main__':
    main(sys.argv[1:])
