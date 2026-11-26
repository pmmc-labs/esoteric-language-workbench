# kind: refused
# perl dies: a file handle (T192, T111).
use v5.42;
my @r = map { say $_ -1 } (5);
