# kind: refused
# perl takes a label in any case (T121, D61).
use v5.42;
my $i = 0;
outer: while ($i++ < 3) {
    last outer;
}
