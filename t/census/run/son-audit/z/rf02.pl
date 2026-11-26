use v5.42;
my @a=(1,2); my @r=map { \$_ } @a; ${$r[0]}=9; print "@a\n";
