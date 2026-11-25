# kind: fault
# model: t/models/list.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2, 3);
    splice(@a, (-3), 1);
    say($a[0]);
}
{
    my @a = (1, 2, 3);
    splice(@a, (-4), 1);
}
say(2);
