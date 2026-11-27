# kind: refused
# perl prints AB: the case escapes are step 16d (D120).
use v5.42;
my $x = "ab";
say qq(\U$x);
