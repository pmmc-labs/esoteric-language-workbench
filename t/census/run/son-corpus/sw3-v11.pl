use v5.42;
my $str = join "", map { chr(ord($_) + 1) } split //, "abc"; print "$str\n";
