# kind: fault
# model: t/models/list.py
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
{
    my @a = (1, 2);
    say(two(@a));
}
{
    my @a = (1, 2, 3);
    say(two(loud('ran'), @a));
}
say(2);
