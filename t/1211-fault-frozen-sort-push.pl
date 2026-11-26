# kind: fault
# model: t/models/sort.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (3, 1, 2);
    my @r = ((sort { $a <=> $b } (@a)));
}
{
    my @a = (3, 1, 2);
    my @r = ((sort { push(@a, 4); $a <=> $b } (@a)));
}
say(2);
