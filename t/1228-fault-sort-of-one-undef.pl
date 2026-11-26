# kind: fault
# model: t/models/sort.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @u = ("");
    my @r = ((sort @u));
}
{
    my @u = ((undef));
    my @r = ((sort @u));
}
say(2);
