# kind: refused
# perl takes it. It is an if written backwards (D54).
use v5.42;
my $x = 0;
unless ($x) {
    say 1;
} else {
    say 2;
}
