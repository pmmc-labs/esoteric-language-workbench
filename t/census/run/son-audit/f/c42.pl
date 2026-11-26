use v5.42;
my @a=(1,2); my $r=\@a; my @b=@$r; $r->[0]=5; print "@b\n";
