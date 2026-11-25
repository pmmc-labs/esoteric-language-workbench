# kind: refused
# Brackets after say change nothing: perl still takes $x for a file
# handle, and dies (T111).
use v5.42;
my $x = 7;
my $y = 2;
say($x +$y);
