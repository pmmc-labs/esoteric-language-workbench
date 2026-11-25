# kind: fault
# model: t/models/list.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
sub two($p, $q) {
    return ($p . ',') . $q;
}
say(1);
{
    my @a = (1);
    say(two(@a, 2));
}
{
    my @a;
    say(two(@a, 2));
}
say(2);
