# kind: fault
# model: t/models/interp.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $n = 9007199254740992.0;
    say("n=${n}.");
}
{
    my $n = 9007199254740991.0;
    say("n=${n}.");
}
say(2);
