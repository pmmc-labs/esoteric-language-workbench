# kind: same
# One reference is thrown as itself, and a catch gets the container (D142, step 13a).
use v5.42;
try { die { code => 42, msg => "bad" }; } catch ($e) { say ref($e), " ", $e->{code}, " ", $e->{msg}; }
try { die [1, 2, 3]; } catch ($e) { say ref($e), " ", $e->[2]; }
my $r = { n => 1 };
try { die $r; } catch ($e) { say $e == $r ? "same" : "other"; $e->{n} = 5; }
say $r->{n};
try { try { die [7]; } catch ($e) { die $e; } } catch ($f) { say $f->[0]; }
