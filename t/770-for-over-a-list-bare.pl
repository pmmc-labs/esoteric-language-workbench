# A loop over a list with no variable is a loop over $_: refused until step
# 10b.
use v5.42;
for (1, 2, 3) {
    say "x";
}
