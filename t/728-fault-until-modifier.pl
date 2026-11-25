# kind: fault
# model: t/models/loop.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $i = 0;
    say($i++) until ($i == 2) || ((10 / (2 - $i)) < 0);
}
{
    my $i = 0;
    say($i++) until (10 / (2 - $i)) < 0;
}
say(2);
