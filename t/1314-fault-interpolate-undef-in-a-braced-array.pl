# kind: fault
# model: t/models/interp.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2);
    say("@{a}s");
}
{
    my @a = ((undef), 2);
    say("@{a}s");
}
say(2);
