# kind: fault
# model: t/models/sort.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @u = ('abc');
    my @r = ((sort { ($a <=> $b) + 0 } (@u)));
}
{
    my @u = ('abc');
    my @r = ((sort { $a <=> $b } (@u)));
}
say(2);
