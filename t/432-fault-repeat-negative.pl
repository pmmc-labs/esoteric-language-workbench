# kind: fault
# model: t/models/list.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @r = (((1, 2) x 0));
    say(scalar(@r));
}
{
    my @r = (((1, 2) x (-1)));
}
say(2);
