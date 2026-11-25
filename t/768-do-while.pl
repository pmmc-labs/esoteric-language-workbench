# kind: refused
# perl runs the block before the first test. It is not a loop to perl,
# and is left out (D58, T64).
use v5.42;
my $i = 0;
do {
    $i++;
} while ($i < 3);
