use v5.42;
use feature 'state'; sub c { state @a; push @a, scalar @a; "@a" } c(); print c(), "\n";
