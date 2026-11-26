use v5.42;
my @a=(1,2); my $r=\@a; push @$r, 3; print "@a\n";
