use v5.42;
my $n = $ENV{X} // 65;
print pack("C3", $n, $n + 1, $n + 2), "\n";
