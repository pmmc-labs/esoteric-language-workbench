# kind: fault
# model: t/models/list.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $u = 2;
    my @r = ((1 .. $u));
    say(scalar(@r));
}
{
    my $u;
    my @r = ((1 .. $u));
}
say(2);
