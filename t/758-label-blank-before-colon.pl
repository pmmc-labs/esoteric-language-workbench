# kind: refused
# perl takes a blank between a label and its colon (T121, D61).
use v5.42;
my $i = 0;
OUTER : while ($i++ < 3) {
    last OUTER;
}
