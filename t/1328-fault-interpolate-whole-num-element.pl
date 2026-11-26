# kind: fault
# model: t/models/interp.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1e+16);
    say("$a[0]");
}
{
    my @a = (1000000000000000.0);
    say("$a[0]");
}
say(2);
