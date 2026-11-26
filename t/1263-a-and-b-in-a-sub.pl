# kind: refused
# perl's $a and $b are a package's, and the sub sees them: 123 (T180).
use v5.42;
sub cmpf() {
    return $a <=> $b;
}
