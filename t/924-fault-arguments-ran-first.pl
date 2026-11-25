# kind: fault
# model: t/models/sub.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
sub two($p, $q) {
    return ($p . ',') . $q;
}
sub loud($p) {
    say($p);
    return $p;
}
say(1);
say(two(loud('a'), loud('b')));
say(two(loud('c'), loud('d'), loud('e')));
say(2);
