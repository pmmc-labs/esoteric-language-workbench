# kind: refused
# perl tests the count of the right side (D78).
use v5.42;
my @a = (1, 2, 3);
if ((my @r = @a)) {
    say "some";
}
