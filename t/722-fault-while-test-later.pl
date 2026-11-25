# kind: fault
# model: t/models/loop.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $i = 0;
    while ((10 / (3 - $i)) > 0) {
        say($i);
        $i++;
        last if $i == 3;
    }
}
{
    my $i = 0;
    while ((10 / (3 - $i)) > 0) {
        say($i);
        $i++;
    }
}
say(2);
