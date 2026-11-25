# kind: fault
# model: t/models/each.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    for my $x (((-9223372036854775295) .. (-9223372036854775294))) {
        say($x);
    }
}
{
    for my $x (((-9223372036854775296) .. (-9223372036854775294))) {
        say($x);
    }
}
say(2);
