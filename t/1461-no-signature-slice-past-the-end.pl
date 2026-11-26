# kind: fault
# A slice past the end among a call's arguments: perl makes the
# elements (T161), whatever the sub does with its arguments (D105).
use v5.42;
my @a = (1);
sub quiet { 1 }
say quiet(@a);
say quiet(@a[3, 4]);
say scalar(@a);
