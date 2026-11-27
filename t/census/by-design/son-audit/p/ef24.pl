use v5.42;
my $x = 1; my $r = \$x; my $a = $$r; $x = 2; my $b = $$r; print "$a$b\n";
