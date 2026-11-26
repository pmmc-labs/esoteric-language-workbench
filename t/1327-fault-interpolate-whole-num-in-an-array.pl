# kind: fault
# model: t/models/interp.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 0.5);
    say("@a");
}
{
    my @a = (1, 1000000000000000.0);
    say("@a");
}
say(2);
