# kind: fault
# model: t/models/interp.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $u = "";
    say("$u");
}
{
    my $u;
    say("$u");
}
say(2);
