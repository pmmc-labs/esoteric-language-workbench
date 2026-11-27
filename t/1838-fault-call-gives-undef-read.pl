# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
sub f() {
    return undef;
}
say(f()->[0]);
say(2);
