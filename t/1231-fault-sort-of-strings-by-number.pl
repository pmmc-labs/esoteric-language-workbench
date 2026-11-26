# kind: fault
# model: t/models/sort.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @u = ('10', '9');
    my @r = ((sort { $a <=> $b } (@u)));
}
{
    my @u = ('10', 'x');
    my @r = ((sort { $a <=> $b } (@u)));
}
say(2);
