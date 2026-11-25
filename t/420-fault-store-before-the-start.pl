# kind: fault
# model: t/models/list.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2, 3);
    $a[(-3)] = 'first';
    say($a[0]);
}
{
    my @a = (1, 2, 3);
    $a[(-4)] = 'x';
}
say(2);
