# kind: refused
# In a while in an if in the block: perl prints 0 and 5 (D77).
use v5.42;
my $p = 1;
my $k = 0;
for my $x (0, $p) {
    if ($x) {
        while ($k < 1) {
            $k++;
            $p = 5;
        }
    }
    say $x;
}
