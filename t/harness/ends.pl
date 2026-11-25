# A loop that ends, and prints a good deal on the way: it must pass.
use v5.42;
my $lines = 0;
while ($lines++ < 20000) { say "a line of output, again and again and again"; }
say $lines;
