use v5.42;
my @h=(1,2); my @c=@h; $c[0]=9; push @h, 3; print "@h;@c\n";
