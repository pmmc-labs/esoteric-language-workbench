# kind: fault
# model: t/models/interp.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $p = 1;
    my $q = 2;
    say("$p$q" + 1);
}
{
    my $p = 1;
    my $q = 'a';
    say("$p$q" + 1);
}
say(2);
