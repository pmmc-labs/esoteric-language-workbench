use v5.42;
my $x="ab"; my $r=\$x; my $s = $x . ($$r =~ tr/a/z/); print "$s\n";
