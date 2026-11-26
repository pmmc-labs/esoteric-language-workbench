# kind: fault
# model: t/models/sort.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (3, 1, 2);
    my @r = ((sort { ($a // 0) <=> ($b // 0) } ($a[2], 5)));
}
{
    my @a = (3, 1, 2);
    my @r = ((sort { ($a // 0) <=> ($b // 0) } ($a[3], 5)));
}
say(2);
