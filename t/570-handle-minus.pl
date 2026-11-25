# kind: refused
# perl takes $x for a file handle, and dies: it is no symbol (T26, T111).
use v5.42;
my $x = 7;
say $x -1;
