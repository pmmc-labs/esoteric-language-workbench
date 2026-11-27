# kind: refused
# perl chops the array's own elements: a c (T9).
use v5.42;
my @a = ("ab", "cd");
for my $x (@a) { chop $x }
