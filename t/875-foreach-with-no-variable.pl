# foreach (LIST): the same loop over $_, refused until step 10b.
use v5.42;
foreach (1, 2) {
    say "x";
}
