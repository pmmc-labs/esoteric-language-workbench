# kind: fault
# model: t/models/interp.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2, 3);
    say("@a[-3 .. -1]");
}
{
    my @a = (1, 2, 3);
    say("@a[-4 .. -3]");
}
say(2);
