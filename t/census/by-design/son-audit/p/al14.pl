use v5.42;
my @a = (1,2,3); my $e = \$a[1]; $$e = 7; print "@a\n";
