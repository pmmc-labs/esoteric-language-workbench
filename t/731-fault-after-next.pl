# kind: fault
# model: t/models/loop.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $i = 0;
    while (($i++) < 3) {
        next if $i >= 2;
        say(6 / (2 - $i));
    }
}
{
    my $i = 0;
    while (($i++) < 3) {
        next if $i == 1;
        say(6 / (2 - $i));
    }
}
say(2);
