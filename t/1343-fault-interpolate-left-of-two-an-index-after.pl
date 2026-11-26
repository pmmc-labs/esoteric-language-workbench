# kind: fault
# model: t/models/interp.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $n = 1e+16;
    my @a = (1, 2, 3);
    my $i = 0;
    say("$n$a[$i]");
}
{
    my $n = 1000000000000000.0;
    my @a = (1, 2, 3);
    my $i = 'x';
    say("$n$a[$i]");
}
say(2);
