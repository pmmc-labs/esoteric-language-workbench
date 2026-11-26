# kind: fault
# model: t/models/interp.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2, 3);
    my $i = ' 2 ';
    say("@a[0, $i]");
}
{
    my @a = (1, 2, 3);
    my $i = "";
    say("@a[0, $i]");
}
say(2);
