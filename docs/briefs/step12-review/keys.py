#!/usr/bin/env python3
"""Keys as strings. The proposal: a key is its expression "made a string as
`.` makes one". For each value, written as a literal, held in a variable
and computed: is `$h{E}` the key that `E . ""` is? Also for a literal
before `=>`, as a slice's key, under `exists` and `delete`, and for a
value with a past (used as a number first, or as a string first).
Reports every place where perl's key is not what `.` gives, or perl warns.

    python3 docs/briefs/step12-review/keys.py
"""
from common import perl

VALUES = ['0', '1', '-1', '7', '1.0', '3.0', '0.5', '.5', '1.50', '-0.0', '0.0', '-0', '1e3', '1e15', '1e16', '1e21', '1e-5', '1.5e300',
          '0x10', '0b11', '0o17', '1_000', '9223372036854775807', '9223372036854775808', '18446744073709551615', '18446744073709551616',
          '-9223372036854775808', '9007199254740992', '9007199254740993', '0.1 + 0.2', '1 / 3', '2 ** 0.5', '10 / 2', '2 ** 62', '2 ** 64', '-2 ** 63',
          '1e15 + 1', '1e15 * 10', '3 * 1.0', '0 * -1', '-0.0 * 1', '0.0 * -1', '1 - 1.0', '-(0.0)', '- 0.0',
          'true', 'false', '!1', '!0', '!!1', '1 == 1', '1 == 2', '"a" eq "a"',
          '"1"', '"1.0"', '"01"', '" 1"', '"1 "', '"1e3"', '"0x10"', '""', '" "', '"a b"', '"-0"', '"+1"', '"0 but true"', '"abc"', '"1" + 0', '"1.0" + 0', '"01" + 0', '"1.0" . ""',
          '"a" . 1', '1 . 1', '"a" x 2', '1 x 3', 'length("abc")', 'ord("a")', 'chr(65)', 'lc("AB")', '1 <=> 2', '"a" cmp "b"', '"b" cmp "a"',
          '(1, 2)[1]', '1 ? 2 : 3', '0 || "z"', 'undef // "d"', '1 . ""', '0 + "3.0"', '"3.0" * 1', '"1e3" + 0', '"1e3" * 1.0', '1.0 * 3', '1e0', '1E3', '6 / 3', '7 / 2', '-7 / 2', '2 ** -1', '10 % 3', '-7 % 3',
          '1.10', '100.0', '1.0e2', '0.000001', '0.0000001', '123456789012345678', '1234567890123456789012', '0.1', '1e100', '-1e-100', '1.5e9', '4294967296', '0xFFFFFFFF']

N = [0]


def one(setup, key_expr, dot_expr):
    """The key perl makes for $h{key_expr}, and the string of dot_expr."""
    N[0] += 1
    return perl('%s my %%h; $h{%s} = 1; my @k = keys %%h; my $d = %s; say "[$k[0]]"; say "[$d]"; say $k[0] eq $d ? "same" : "DIFFERENT";' % (setup, key_expr, dot_expr))


def report(what, v, r):
    out, err, code = r
    if code != 0 or err or not out.endswith('same\n'):
        print('%-22s %-28s %s %s' % (what, v, out.replace('\n', ' '), ('| ' + err.strip().split('\n')[0][:110]) if err else ''))


def main():
    for v in VALUES:
        report('literal in braces', v, one('', v, '(%s) . ""' % v))
        report('in brackets', v, one('', '(%s)' % v, '(%s) . ""' % v))
        report('in a variable', v, one('my $v = %s;' % v, '$v', '$v . ""'))
        report('computed', v, one('my $v = %s;' % v, '$v . ""', '$v . ""'))
        report('through a sub', v, one('sub f() { return %s } ' % v, 'f()', 'f() . ""'))
        report('used as a number', v, one('no warnings; my $v = %s; my $n = $v + 0; use warnings;' % v, '$v', '$v . ""'))
        report('used as a string', v, one('my $v = %s; my $s = "$v";' % v, '$v', '$v . ""'))
        report('interpolated', v, one('my $v = %s;' % v, '"$v"', '$v . ""'))
        # before =>: a literal there is "the number, made a string"
        N[0] += 1
        report('before =>', v, perl('my %%h = (%s => 1); my @k = keys %%h; my $d = (%s) . ""; say "[$k[0]]"; say "[$d]"; say $k[0] eq $d ? "same" : "DIFFERENT";' % (v, v)))
        N[0] += 1
        report('slice', v, perl('my %%h; my @s = (1, 2); @h{%s, "zz"} = @s; my @k = grep { $_ ne "zz" } keys %%h; my $d = (%s) . ""; say "[$k[0]]"; say "[$d]"; say $k[0] eq $d ? "same" : "DIFFERENT";' % (v, v)))
        N[0] += 1
        report('exists and delete', v, perl('my $v = %s; my %%h = ($v . "", 5); say exists $h{%s} ? "same" : "DIFFERENT"; say delete($h{$v}) // "DIFFERENT"; say scalar(%%h) == 0 ? "same" : "DIFFERENT";' % (v, v)))
        N[0] += 1
        report('in a string', v, perl('my $v = %s; my %%h = ($v . "", 5); say "$h{$v}" eq "5" ? "same" : "DIFFERENT";' % v))
    print('%d programs' % N[0])


main()
