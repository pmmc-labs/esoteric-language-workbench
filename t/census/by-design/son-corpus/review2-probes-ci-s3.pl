use v5.42;
sub f { my ($a, $b) = @_; if ($a > $b) { print "gt\n" } return $a - $b }
print f(5, 2), "\n";
