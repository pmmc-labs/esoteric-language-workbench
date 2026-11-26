use v5.42;
my @a=("a","b"); my @b=map { $_ .= "!" ; $_ } @a; print "@a|@b\n";
