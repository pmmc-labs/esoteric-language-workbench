use v5.42;
my @a = (10, 20);
my $s = \@a;
print "$$s[0] $$s[1]\n";
