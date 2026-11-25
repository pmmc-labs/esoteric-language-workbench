# kind: fault
# model: t/models/list.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
sub loud($p) {
    say($p);
    return $p;
}
say(1);
{
    my @a = (1, 2, 3);
    $a[0] .= loud('heard');
    say($a[0]);
}
{
    my @a = (1, 2, 3);
    $a[(-4)] .= loud('not heard');
}
say(2);
