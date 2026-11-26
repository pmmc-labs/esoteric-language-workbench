use v5.42;
our @g = (3,1,2); my @s = sort { $a <=> $b } @g; @g = (); print "@s\n";
