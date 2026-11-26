use v5.42;
my @a=(1,2,3); my ($f,@r) = @a; @a = (@r, $f); print "@a\n";
