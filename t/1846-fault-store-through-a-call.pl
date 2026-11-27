# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
sub f() {
    return undef;
}
f()->[0] = 5;
say(2);
