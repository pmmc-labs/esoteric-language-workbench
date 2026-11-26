use v5.42;
my $n = $ENV{X} // 2;
my $r = eval "$n + 1";
print "$r\n";
