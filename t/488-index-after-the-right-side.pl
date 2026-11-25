# kind: refused
# perl stores 99: the right side is read after the index has run (T158, D76).
use v5.42;
my @a = (1, 2, 3);
sub bump() { $a[0] = 99; return 1; }
$a[bump()] = $a[0];
say $a[1];
