# kind: fault
# model: t/models/interp.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2);
    my @r = ((map { "$_-" } (@a)));
}
{
    my @a = (1, (undef));
    my @r = ((map { "$_-" } (@a)));
}
say(2);
