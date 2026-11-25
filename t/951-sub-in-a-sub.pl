# kind: refused
# perl warns: Variable "$x" will not stay shared (T31).
use v5.42;
sub outer($x) {
    sub inner() { return $x; }
    return inner();
}
say outer(1);
