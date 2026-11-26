# kind: fault
# model: t/models/hash.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
sub count($x, %o) {
    return scalar(keys(%o));
}
say(1);
say(count(1));
say(count());
say(2);
