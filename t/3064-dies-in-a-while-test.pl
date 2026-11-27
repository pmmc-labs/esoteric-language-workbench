# kind: dies
# In a while's test, written to end in a newline (D150).
use v5.42;
my $i = 0;
while ($i < 3 || die "ran out\n") {
    $i++;
    say $i;
}
