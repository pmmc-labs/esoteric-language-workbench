use v5.42;
use feature 'state'; sub t { print "t"; 5 } sub c { state $n = t(); $n++ } print c(), c(), "\n";
