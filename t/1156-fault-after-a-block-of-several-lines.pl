# kind: fault
# A fault after a block, in the statement the block stands in, names the
# line that statement starts on, and not the block's last line. By hand.
use v5.42;
my @a = (1, 2);
my $u;
say 1;
my @r = ((map {
    $_ + 1
} @a), 5);
say @r;
my @s = ((map {
    $_ + 1
} @a), $u + 1);
say 2;
