# kind: fault
# The largest index a string takes, 2^63 - 1, from either end: past the
# end, an undef. perl warns, and one more is refused (T211).
use v5.42;
my @a = (1, 2, 3);
say "$a[2]";
say "<$a[9223372036854775807]>";
say "<$a[-9223372036854775807]>";
