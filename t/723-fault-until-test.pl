# kind: fault
# model: t/models/loop.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $i = 2;
    until (($i == 0) || ((10 / $i) < 2)) {
        say($i);
        $i--;
    }
}
{
    my $i = 2;
    until ((10 / $i) < 2) {
        say($i);
        $i--;
    }
}
say(2);
