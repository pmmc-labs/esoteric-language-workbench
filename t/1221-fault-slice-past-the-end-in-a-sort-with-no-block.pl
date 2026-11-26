# kind: fault
# model: t/models/sort.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (3, 1, 2);
    my @r = ((sort @a[0, 2]));
}
{
    my @a = (3, 1, 2);
    my @r = ((sort @a[0, 3]));
}
say(2);
