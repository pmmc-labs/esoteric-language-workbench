# By hand, with perl's answers: what the breakages of step 13a showed no
# test reached (docs/briefs/step13a-mutations.py).
use v5.42;
my $r = [1];
my $o = $r;
sub swap() {
    $r = [5];
    return 7;
}
# The right side first, and then the chain: the store is to the new array.
$r->[0] = swap();
say $r->[0], $o->[0];
# A list assignment makes what its targets go through.
my $m;
($m->[0], $m->[1]{k}) = (7, 8);
say ref($m), $m->[0], $m->[1]{k};
# A reference in a loop's list freezes nothing: the list holds the
# reference, not the array's elements.
my @a = (1);
for my $ra (\@a) {
    push @a, 2;
    say scalar(@a), $ra->[1];
}
# A new array is no constant, and a test of one is no mistake.
if (my $t = [1]) {
    say "tested";
}
# After a new hash, as after any value, comes an operator.
say(({} and 1) ? "t" : "f");
