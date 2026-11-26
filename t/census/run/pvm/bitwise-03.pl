use v5.42;
my $a = $ENV{X} // 1;
my $b = $ENV{Y} // 16;
print $a << 3, " ", $b >> 2, "\n";
