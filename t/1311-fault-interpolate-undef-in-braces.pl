# kind: fault
# model: t/models/interp.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $u = 0;
    say("a${u}b");
}
{
    my $u;
    say("a${u}b");
}
say(2);
