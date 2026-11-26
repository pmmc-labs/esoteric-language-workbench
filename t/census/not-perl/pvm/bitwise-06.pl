use v5.42;
use v5.28;
my $s1 = $ENV{X} // "12";
my $s2 = $ENV{Y} // "10";
print $s1 & $s2, "\n";
