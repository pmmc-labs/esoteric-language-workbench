# perl hands g no argument, and prints g's default (T143): a list
# repeated no times is no value. A list from step 9 (D80); until then
# this test was of its refusal.
use v5.42;
sub g($p = "d") { return $p; }
my $n = 0;
say g(("a") x $n);
$n = 1;
say g(("a") x $n);
