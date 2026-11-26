# kind: fault
# model: t/models/interp.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my @a = (1, 2);
sub f($s) {
    return $s;
}
say(1);
say(f("@a"));
say(f("$a[5]"));
say(2);
