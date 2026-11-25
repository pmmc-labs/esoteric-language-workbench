# kind: fault
# model: t/models/sub.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
sub a($p) {
    return 1 + b($p);
}
sub b($p) {
    return 1 + c($p);
}
sub c($p) {
    return 7 % $p;
}
say(1);
say(a(2));
say(a(0));
say(2);
