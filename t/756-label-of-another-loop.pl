# kind: refused
# The label is on a loop this next is not in. perl dies as it runs:
# Label not found for "next A" (T121).
use v5.42;
my $i = 0;
A: while ($i++ < 2) {
    say $i;
}
while ($i++ < 5) {
    next A;
}
