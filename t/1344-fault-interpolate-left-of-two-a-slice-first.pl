# kind: fault
# model: t/models/interp.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2);
    my $u = 0;
    say("@a[0, 1]$u");
}
{
    my @a = (1, 1000000000000000.0);
    my $u;
    say("@a[0, 1]$u");
}
say(2);
