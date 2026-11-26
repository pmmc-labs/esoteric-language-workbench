use v5.42;
our @g = (1,2); my $r = \@g; @g = (3); print "@$r\n";
