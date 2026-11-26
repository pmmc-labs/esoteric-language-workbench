use v5.42;
sub f { my $n = shift; return defined($n) ? "def" : "undef" } print f($ENV{CHALK_NOPE_XYZ}), "\n";
