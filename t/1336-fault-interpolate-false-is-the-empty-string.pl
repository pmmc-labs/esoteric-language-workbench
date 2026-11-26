# kind: fault
# model: t/models/interp.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $t = true;
    say("$t" + 1);
}
{
    my $t = false;
    say("$t" + 1);
}
say(2);
