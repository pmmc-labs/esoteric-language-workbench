# kind: fault
# model: t/models/sort.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @u = ('b', "", 'a');
    my @r = ((sort @u));
}
{
    my @u = ('b', (undef), 'a');
    my @r = ((sort @u));
}
say(2);
