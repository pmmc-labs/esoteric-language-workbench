use v5.42;
my @a = do { (1,2,3) }; my $c = do { 1; 2 }; print "@a $c\n";
