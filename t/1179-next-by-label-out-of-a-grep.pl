# kind: refused
# The same, by its label (T59).
use v5.42;
OUT: for my $i (1 .. 3) {
    my @r = grep { next OUT; 1 } (1, 2, 3);
    say $i;
}
