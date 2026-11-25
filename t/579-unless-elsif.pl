# kind: refused
# perl takes it (D54).
use v5.42;
my $x = 0;
unless ($x) {
    say 1;
} elsif ($x) {
    say 2;
}
