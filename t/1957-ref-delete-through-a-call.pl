# kind: refused
# perl runs it, and says nothing.
use v5.42;
sub f() {
    return {};
}
delete f()->{a};
