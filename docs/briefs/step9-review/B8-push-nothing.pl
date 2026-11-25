use v5.42;
my @a;
push @a;
unshift(@a);
push @a, ();
say scalar(@a);
