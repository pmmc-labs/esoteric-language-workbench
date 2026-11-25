# kind: refused
# perl 5.36 and later: two values at a time.
use v5.42;
for my ($k, $v) (1, 2, 3, 4) {
    say $k;
}
