use v5.42;
our @g = (1,2); push @g, 3; my @c = (@g); push @g, 4; print "@c|@g\n";
