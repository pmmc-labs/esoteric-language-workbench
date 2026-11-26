use v5.42;
use feature 'state'; sub c { state @l; push @l, shift; scalar @l } c(1); print c(2), "\n";
