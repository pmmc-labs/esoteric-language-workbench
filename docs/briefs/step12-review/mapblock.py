#!/usr/bin/env python3
"""`my %h = map { KEY => VALUE } LIST;`: perl guesses from the first tokens
after `{` whether it is a block or a hash in braces, and a wrong guess is a
syntax error at the `}` (T175 has the rule for a comma; `=>` is a comma).
For each way a block can begin: does perl take it as a block, in silence?

    python3 docs/briefs/step12-review/mapblock.py
"""
from common import perl

FIRSTS = ['$_ => 1', '"$_" => 1', '"k" => $_', "'k' => $_", '"k$_" => 1', '"${_}" => 1', 'k => $_', 'lc($_) => 1', 'lc $_ => 1', 'uc => 1', '($_ => 1)', '+($_ => 1)',
          '; $_ => 1', ';"$_" => 1', '+"$_" => 1', '$h{$_} => 1', '$_, 1', '"$_", 1', '"a", 1', '1 => $_', '1.5 => $_', '$_ . "x" => 1', '"x" . $_ => 1', '-$_ => 1',
          '@a => 1', 'my $k = $_; $k => 1', '$_ => $_ * 2', '$k => 1', 'true => $_', 'q => $_', 'x => $_', '$_ => 1,', '$_ => 1;', '$_',
          '"$_"', '"$_" . "x" => 1', '"$_" x 2 => 1', '"a$k" => 1', '$a[0] => 1', '$g{a} => 1', '%g', '%g, $_ => 1', '%g => 1', 'K => 1', 'f($_) => 1', 'f => 1', '(f($_)) => 1',
          '"a" . "b" => 1', '"a" => 1, "b" => 2', '$_ => "v"', '$_ => "$_"', "$_ => 'v'", '{ $_ => 1 }', '+{ $_ => 1 }', '"$_", "v"', '"\\$x" => 1', '"a\\n" => 1', "'' => 1", '"" => 1',
          'undef => 1', 'undef, 1', '-1 => $_', '.5 => $_', '0x10 => $_', '$_=>1', '"$_"=>1', '$_ ,1', ' $_ => 1', '\n$_ => 1\n', '\n"$_" => 1\n', '# c\n "$_" => 1']
HEAD = 'my @a = ("p", "q"); my %g = (a => "b"); my $k = "kk"; sub f($x) { return "f" . $x } my %h = map { '
TAIL = ' } @a; say join ",", map { "$_=$h{$_}" } sort keys %h;'


def main():
    for first in FIRSTS:
        out, err, code = perl(HEAD + first + TAIL)
        if code == 0 and not err:
            what = 'a block: ' + out.strip()
        elif code == 0:
            what = 'a block, WARNS: %s -> %s' % (err.strip().split('\n')[0][:80], out.strip())
        else:
            what = 'perl stops: ' + err.strip().split('\n')[0][:100]
        print('  map { %-22s }  %s' % (first.replace('\n', '\\n'), what))
    print('%d programs' % len(FIRSTS))


main()
