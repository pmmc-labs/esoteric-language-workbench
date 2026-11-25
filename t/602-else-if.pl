# kind: refused
# perl doesn't compile it either: the word is elsif.
use v5.42;
my $x = 0;
if ($x) {
    say 1;
} else if ($x == 0) {
    say 2;
}
