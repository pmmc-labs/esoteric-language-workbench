# kind: fault
# model: t/models/interp.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2, 3);
    my $i = '1';
    say("$a[$i]");
}
{
    my @a = (1, 2, 3);
    my $i = 'one';
    say("$a[$i]");
}
say(2);
