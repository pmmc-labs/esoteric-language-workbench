# kind: refused
# The same for a last statement (T16): step 10.
use v5.42;
my @a = (1, 2, 3);
sub g() { @a }
my $n = g();
say $n;
