# kind: refused
# perl has one global $_, and prints 24 (T180, T15): here a sub can not see it.
use v5.42;
sub show() {
    return $_ * 2;
}
my @s = map { show() } (1, 2);
say @s;
