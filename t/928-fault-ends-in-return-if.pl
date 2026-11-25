# kind: fault
# model: t/models/sub.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
sub ends($p) {
    return 'yes' if $p;
}
say(1);
say(ends(1));
say(ends(0));
say(2);
