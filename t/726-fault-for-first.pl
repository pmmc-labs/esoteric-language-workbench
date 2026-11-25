# kind: fault
# model: t/models/loop.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $v = 5;
    for (my $i = (10 / $v); $i < 4; $i++) {
        say($i);
    }
}
{
    my $v = 0;
    for (my $i = (10 / $v); $i < 4; $i++) {
        say($i);
    }
}
say(2);
