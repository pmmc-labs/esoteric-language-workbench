# kind: fault
# model: t/models/loop.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    for (my $i = 9223372036854775805, my $k = 0; $k < 2; $i++, $k++) {
        say($i);
    }
}
{
    for (my $i = 9223372036854775805, my $k = 0; $k < 5; $i++, $k++) {
        say($i);
    }
}
say(2);
