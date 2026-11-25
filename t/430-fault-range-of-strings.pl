# kind: fault
# model: t/models/list.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @r = ((1 .. 3));
    say(scalar(@r));
}
{
    my @r = (('1' .. '3'));
}
say(2);
