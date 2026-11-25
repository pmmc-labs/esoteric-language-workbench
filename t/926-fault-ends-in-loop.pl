# kind: fault
# model: t/models/sub.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
sub ends($p) {
    my $i = 0;
    while ($i < $p) {
        $i++;
    }
}
say(1);
ends(2);
say(ends(2) + 1);
say(2);
