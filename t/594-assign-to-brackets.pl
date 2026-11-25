# A list assignment, to perl (D56), and from step 9 to the language
# (D78): one target, which takes the first value. Until then this test
# was of its refusal.
use v5.42;
my $x;
($x) = 5;
say $x;
($x) = (7, 8, 9);
say $x;
