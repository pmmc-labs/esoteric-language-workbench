# kind: fault
# A fault after a sort, in the statement it stands in, names the line that
# statement starts on, and not the block's last line. By hand.
use v5.42;
my @a = (2, 1);
my $u;
say 1;
my @r = ((sort {
    $a <=> $b
} @a), 5);
say @r;
my @s = ((sort {
    $a <=> $b
} @a), $u + 1);
say 2;
