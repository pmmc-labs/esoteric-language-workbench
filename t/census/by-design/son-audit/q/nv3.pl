use v5.42;
our @g = (1,2); my @c = @g; push @g, 3; print "@c\n";
