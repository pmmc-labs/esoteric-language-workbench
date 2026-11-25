# kind: refused
# When the test fails perl leaves in the variable what it last held,
# which is documented as undefined behaviour (T30).
use v5.42;
my $y = 0;
my $x = 5 if $y;
