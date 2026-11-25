# kind: fault
# model: t/models/list.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2, 3);
    splice(@a, 3, 0, 9);
    say($a[3]);
}
{
    my @a = (1, 2, 3);
    splice(@a, 4, 0, 9);
}
say(2);
