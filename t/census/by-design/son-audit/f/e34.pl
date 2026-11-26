use v5.42;
use feature 'try'; no warnings; try { die "a\n" } catch ($e) { print "[$@]$e" }
