# kind: refused
# perl prints a, then b.
use v5.42;
print <<A, <<B;
a
A
b
B
