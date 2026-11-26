# kind: fault
# model: t/models/hash.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
sub take($x, %) {
    return $x;
}
say(1);
say(take(1, 2, 3));
say(take(1, 2));
say(2);
