use v5.42;
sub f { return ("a","b") } my ($x) = f(); my $y = f(); my $c = () = f(); print "$x$y$c\n";
