use v5.42;
my $s = "abc"; my $r = \$s; my $a = length($$r); $s = "x"; my $b = length($$r); print "$a$b\n";
