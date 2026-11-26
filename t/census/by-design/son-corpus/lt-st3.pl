use v5.42;
sub w { my ($a, $b) = @_; return $a && $b } print w(1, 2), "|", w("x", "y"), "\n";
