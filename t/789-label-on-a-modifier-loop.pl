# kind: refused
# perl takes a label there, and it does nothing: a statement with a
# while after it is no loop to last or next (T121).
use v5.42;
my $i = 0;
L: $i++ while $i < 3;
