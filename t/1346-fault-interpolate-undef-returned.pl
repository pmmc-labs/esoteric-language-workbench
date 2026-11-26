# kind: fault
# model: t/models/interp.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
sub f($s) {
    return "<$s>";
}
say(1);
say(f(1));
say(f((undef)));
say(2);
