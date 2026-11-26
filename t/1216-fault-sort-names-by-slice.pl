# kind: fault
# model: t/models/sort.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (3, 1, 2);
    my @b = (7);
    my @r = ((sort { $a <=> $b } (@a[0, 1])));
}
{
    my @a = (3, 1, 2);
    my @b = (7);
    my @r = ((sort { $a[0] = 9; $a <=> $b } (@a[0, 1])));
}
say(2);
