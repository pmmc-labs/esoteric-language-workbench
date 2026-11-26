# kind: fault
# model: t/models/sort.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (3, 1, 2);
    my @r = ((sort { 2147483647 } (@a)));
}
{
    my @a = (3, 1, 2);
    my @r = ((sort { 2147483648 } (@a)));
}
say(2);
