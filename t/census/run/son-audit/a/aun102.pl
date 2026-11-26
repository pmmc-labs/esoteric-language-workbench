use v5.42;
my @a=(1,2); my $r=\@a; my @b=@$r; push @a,3; print "@b|@a\n";
