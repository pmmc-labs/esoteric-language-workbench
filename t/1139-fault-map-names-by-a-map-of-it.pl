# kind: fault
# model: t/models/it.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2, 3);
    my @b = (7);
    my @r = ((map { $_ + 0 } ((map { $_ } (@a)))));
}
{
    my @a = (1, 2, 3);
    my @b = (7);
    my @r = ((map { $a[0] = 9; $_ + 0 } ((map { $_ } (@a)))));
}
say(2);
