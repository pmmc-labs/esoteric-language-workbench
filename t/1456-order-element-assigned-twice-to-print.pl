# kind: refused
# perl prints 77 (T213).
use v5.42;
my @a = (1);
print $a[0] = 5, $a[0] = 7;
print "\n";
