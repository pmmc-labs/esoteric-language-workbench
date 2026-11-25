# kind: refused
# perl takes $x for a file handle and .5 for a number, and dies (T111).
use v5.42;
my $x = 7;
print $x .5;
