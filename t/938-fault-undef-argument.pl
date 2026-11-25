# kind: fault
# model: t/models/sub.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
sub len($p = (undef)) {
    return $p + 1;
}
say(1);
say(len(1));
say(len());
say(2);
