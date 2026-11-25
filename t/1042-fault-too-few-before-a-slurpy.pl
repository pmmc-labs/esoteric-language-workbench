# kind: fault
# model: t/models/ret.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
sub f($p, $q, @rest) {
    return 1;
}
say(1);
say(f(1, 2));
say(f(1));
say(2);
