# kind: refused
# perl takes $x for a file handle and the slash for the start of a
# pattern, and doesn't compile (T111).
use v5.42;
my $x = 7;
say $x /2;
