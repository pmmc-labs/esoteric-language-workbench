# kind: refused
# an interpolated string is such a row: kk-v (T230).
use v5.42;
my %g;
my $i = "a";
$g{$i = "k"} = "$i-v";
say %g;
