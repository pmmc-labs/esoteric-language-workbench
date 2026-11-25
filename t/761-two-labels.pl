# kind: refused
# Only the label nearest the loop names it: perl dies as it runs, Label
# not found for "last A" (T121).
use v5.42;
my $i = 0;
A: B: while ($i++ < 3) {
    last A;
}
