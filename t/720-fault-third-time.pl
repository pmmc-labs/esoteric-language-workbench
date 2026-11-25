# kind: fault
# model: t/models/loop.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $i = 0;
    while ($i < 2) {
        say(10 / (2 - $i));
        $i++;
    }
}
{
    my $i = 0;
    while ($i < 3) {
        say(10 / (2 - $i));
        $i++;
    }
}
say(2);
