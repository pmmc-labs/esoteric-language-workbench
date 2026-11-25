# kind: refused
# In the third part of a loop of three parts, in the block (D77).
use v5.42;
my $p = 1;
for my $x ($p) {
    for (my $i = 0; $i < 2; $i++, $p++) {
        say $i;
    }
    say $x;
}
