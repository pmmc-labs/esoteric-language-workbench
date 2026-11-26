use v5.42;
our @g = (1,2); my $s = "@g"; @g = (9); print "$s\n";
