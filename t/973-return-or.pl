# kind: refused
# perl warns: Possible precedence issue with control flow operator (return) (T139).
use v5.42;
sub f($v) {
    return $v or 9;
}
say f(3);
