use v5.42;
our @st = (1); my @c = (@st, 2); @st = (); print "@c\n";
