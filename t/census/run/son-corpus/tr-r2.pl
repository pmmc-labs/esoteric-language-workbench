use v5.42;
my $s = "hello"; my $n = ($s =~ tr/a-y/b-z/); print "$s $n\n";
