use v5.42;
sub c { wantarray ? "L" : "S" } print "a" . c(), "b", c(), "\n"; print c() . "\n";
