# A list of variables (D80, step 9): each is declared, and undef. Until
# then this test was of its refusal.
use v5.42;
my ($x, $y);
say defined($x) ? "defined" : "undef";
$y = 2;
say $y;
