# kind: fault
# model: t/models/sub.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
sub two($p, $q) {
    return ($p . ',') . $q;
}
say(1);
say(two(1, 2));
say(two(1, 2, 3));
say(2);
