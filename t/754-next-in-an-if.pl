# kind: refused
# An if's block is no loop. perl dies as it runs: Can't "next" outside a
# loop block.
use v5.42;
my $i = 0;
if ($i == 0) {
    next;
}
