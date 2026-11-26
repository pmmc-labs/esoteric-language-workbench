use v5.42;
my $a = $ENV{X} // 6;
my $b = $ENV{Y} // 3;
my $c = $ENV{Z} // 2;
print $a | $b & $c, " ", ($a | $b) & $c, "\n";
