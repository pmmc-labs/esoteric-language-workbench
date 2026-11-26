use v5.42;
my $r = do { my $t = $ENV{X} // 7; $t + 1 };
print "$r\n";
