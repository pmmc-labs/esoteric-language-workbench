# kind: fault
# model: t/models/sub.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
sub div($p) {
    say('in');
    return $p;
}
say(1);
say(10 / div(5));
say(10 / div(0));
say(2);
