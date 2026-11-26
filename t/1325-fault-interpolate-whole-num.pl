# kind: fault
# model: t/models/interp.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $n = 999999999999999.0;
    say("$n");
}
{
    my $n = 1000000000000000.0;
    say("$n");
}
say(2);
