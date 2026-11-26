use v5.42;
my @w = qw(pear Apple fig apple Pear FIG); my @s = sort { lc $a cmp lc $b } @w; print "@s\n";
