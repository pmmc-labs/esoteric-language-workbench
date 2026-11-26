use v5.42;
my $a = $ENV{X} // 12;
print $a & 10, " ", $a | 3, " ", $a ^ 3, "\n";
