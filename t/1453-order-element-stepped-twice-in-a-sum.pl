# kind: refused
# perl prints 6 (T213).
use v5.42;
my @a = (1);
my $n = ++$a[0] + ++$a[0];
say $n;
