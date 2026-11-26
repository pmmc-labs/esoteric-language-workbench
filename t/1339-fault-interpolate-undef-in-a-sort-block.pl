# kind: fault
# model: t/models/interp.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (2, 1);
    my @r = ((sort { "$a" cmp "$b" } (@a)));
}
{
    my @a = (2, (undef));
    my @r = ((sort { "$a" cmp "$b" } (@a)));
}
say(2);
