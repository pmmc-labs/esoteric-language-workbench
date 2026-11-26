# kind: fault
# model: t/models/interp.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $u = "";
    my @a = (1);
    say("$u@a");
}
{
    my $u;
    my @a = (1000000000000000.0);
    say("$u@a");
}
say(2);
