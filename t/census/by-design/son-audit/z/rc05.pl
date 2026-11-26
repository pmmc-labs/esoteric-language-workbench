use v5.42;
use feature 'state'; sub c { state $n=0; ++$n } c(); print c(), "\n";
