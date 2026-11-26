use v5.42;
my $s = "abc"; my $r = \$s; my $l = length $s; $$r .= "d"; print "$l ", length($s), "\n";
