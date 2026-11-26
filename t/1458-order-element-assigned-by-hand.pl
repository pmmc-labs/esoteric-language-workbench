# An assignment to an element as an operand and as a list's item, where
# nothing after it changes the array: what perl prints (T213).
use v5.42;
my @a = (1, 2);
my $n = ($a[0] = 5) + 1;
my $m = ($a[0] += 1) + $a[1];
say ++$a[1] + 1;
my @l = ($a[0] = 3, 4);
say "$n $m @l @a";
my @b = (1);
my $s = ($b[0] = 5) + ($a[0] = 7);
say "$s @a @b";
