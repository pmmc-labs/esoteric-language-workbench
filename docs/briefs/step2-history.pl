# Where does a number's past show? For each value, each earlier use of it
# and each later look at it: does the look give a different answer than it
# gives with no earlier use? Step 2's proposal (docs/PLAN.md) rests on the
# answer, which under perl 5.42.0 is: in two places only. A whole float
# from 1e15 to 2^53 - 1 prints as a float before it has been used as an
# integer and as an integer after (and so do its negation and its
# decrement); and the negation of a float zero is a negative zero before,
# and a plain one after, which atan2 can see.
#
#     $CURLY_PERL docs/briefs/step2-history.pl
#
# Everything here is ordinary Perl, most of it outside the language. Not
# part of make test: add a value, a use or a look when a step brings one.
use v5.42;
no warnings;
my @values = (
    '0.0', '-0.0', '0/5', '0/-5', '0*-1.5', '1.5-1.5', '1.0', '-1.0', '3.0', '1.5', '-2.5', '1e3', '1e14',
    '999999999999999.0', '1e15', '-1e15', '2e15', '4000000000000000/2', '2**50', '2**52', '9007199254740991.0',
    '9007199254740992.0', '-9007199254740992.0', '1e16', '1e17', '2**62', '2**63', '1e19', '1.8e19', '2**64', '1e20', '1e300',
    '9**9**9', '-9**9**9', '9**9**9-9**9**9',
    '0', '1', '1000000000000000', '9007199254740993', '9223372036854775807', '-9223372036854775807-1',
);
my %uses = (
    'add'      => 'my $t = $x + 1;',
    'compare'  => 'my $t = $x == 1;',
    'order'    => 'my $t = $x <=> 1;',
    'modulus'  => 'my $t = $x % 7;',
    'int'      => 'my $t = int($x);',
    'string'   => 'my $t = "$x";',
    'index'    => 'my @a = (1); my $t = $a[$x];',
    'negate'   => 'my $t = -$x;',
    'abs'      => 'my $t = abs($x);',
    'multiply' => 'my $t = $x * 1.5;',
    'divide'   => 'my $t = $x / 2;',
    'power'    => 'my $t = $x ** 2;',
    'bits'     => 'my $t = $x & 1;',
    'sprintf-d'=> 'my $t = sprintf("%d", $x);',
    'sort'     => 'my @s = sort { $a <=> $b } ($x, 2);',
    'truth'    => 'my $t = $x ? 1 : 0;',
    'string-then-add' => 'my $t = "$x"; my $u = $x + 1;',
);
my %looks = (
    'say'      => '$x',
    'negate'   => '-$x',
    'abs'      => 'abs($x)',
    'int'      => 'int($x)',
    'add 0'    => '$x + 0',
    'times 1'  => '$x * 1',
    'over 1'   => '$x / 1',
    'power 1'  => '$x ** 1',
    'mod 1000' => '$x % 1000',
    '0 minus'  => '0 - $x',
    'times -1' => '$x * -1',
    'neg neg'  => '- -$x',
    'neg add 0'=> '-$x + 0',
    'concat'   => '$x . ""',
    'sprintf-s'=> 'sprintf("%s", $x)',
    'sprintf-g'=> 'sprintf("%g", $x)',
    'sprintf-d'=> 'sprintf("%d", $x)',
    'sprintf-.17g' => 'sprintf("%.17g", $x)',
    'one over' => '1 / $x',
    'atan2'    => 'atan2(0, $x)',
    'atan2 neg'=> 'atan2(0, -$x)',
    'equal 0'  => '($x == 0 ? "y" : "n")',
    'truth'    => '($x ? "t" : "f")',
    'half'     => '$x / 2',
    'squared'  => '$x ** 2',
    'plus half'=> '$x + 0.5',
    'postinc'  => 'do { my $y = $x; $y++; $y }',
    'predec'   => 'do { my $y = $x; --$y; $y }',
    'bits'     => '$x | 0',
    'compare'  => '($x <=> 5)',
    'length'   => 'length($x)',
);
my $look = sub ($value, $use, $look) {
    my $r = eval "my \$x = $value; $use; my \$r = $look; \"\$r\"";
    return defined $r ? $r : "died: " . ($@ =~ s/ at .*//sr);
};
my %by_look;
for my $v (@values) {
    for my $l (sort keys %looks) {
        my $plain = $look->($v, '', $looks{$l});
        for my $u (sort keys %uses) {
            my $after = $look->($v, $uses{$u}, $looks{$l});
            next if $after eq $plain;
            push $by_look{$l}{"$v: $plain -> $after"}->@*, $u;
        }
    }
}
for my $l (sort keys %by_look) {
    say "$l:";
    say "    $_   after: @{ $by_look{$l}{$_} }" for sort keys $by_look{$l}->%*;
}
