# kind: refused
# A sub can not see how it was called (D18).
use v5.42;
sub f() {
    return wantarray;
}
say f();
