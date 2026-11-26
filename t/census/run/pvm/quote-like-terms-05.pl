use v5.42;
my $x = $ENV{X} // 1;
print qq{a{b}c=$x}, qq(p), qq[q], qq!r!, "\n";
