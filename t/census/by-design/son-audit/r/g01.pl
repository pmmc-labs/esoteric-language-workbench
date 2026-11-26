use v5.42;
our $g=1; sub f { $g=2; 0 } my $v = $g . f() . $g; print "$v\n";
