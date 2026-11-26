use v5.42;
my @a = (1,2); my $r = \@a; @a = (3,4); print "@$r\n";
