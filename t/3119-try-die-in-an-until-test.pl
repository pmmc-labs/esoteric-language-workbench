# kind: refused
# perl: u at the line of the if (T316).
use v5.42;
my $j = 0;
until ($j >= 1 && die "u") { $j++; }
