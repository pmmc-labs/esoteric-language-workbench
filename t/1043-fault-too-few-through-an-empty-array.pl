# kind: fault
# model: t/models/ret.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my @e;
sub f($p, @rest) {
    return 1;
}
say(1);
say(f(@e, 1));
say(f(@e));
say(2);
