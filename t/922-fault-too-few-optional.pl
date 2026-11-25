# kind: fault
# model: t/models/sub.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
sub opt($p, $q = 2, $r = 3) {
    return ((($p . ',') . $q) . ',') . $r;
}
say(1);
say(opt(1));
say(opt());
say(2);
