# kind: refused
# A loop over a list with no variable is a loop over $_, to perl.
use v5.42;
for (1, 2, 3) {
    say "x";
}
