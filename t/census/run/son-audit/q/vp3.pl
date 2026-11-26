use v5.42;
my $s = "abc"; my $old = substr($s, 0, 1, "X"); print "$old $s\n";
