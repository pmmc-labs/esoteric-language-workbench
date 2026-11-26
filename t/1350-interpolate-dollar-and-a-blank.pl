# kind: refused
# perl reads `$b`, with the blank: a 7 (T200).
use v5.42;
my $b = 7;
say "a $ b";
