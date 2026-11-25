# kind: refused
# A range is fixed as the loop starts, to perl too, which prints 1, 2, 3:
# refused by the one rule all the same (D77). The end in a my of its
# own, or as a call's value, says it.
use v5.42;
my $n = 3;
for my $i (1 .. $n) {
    $n = 1;
    say $i;
}
