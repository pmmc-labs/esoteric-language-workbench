# kind: fault
# model: t/models/each.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    for my $x ((1 .. 2)) {
        say($x);
    }
}
{
    for my $x ((1 .. '2')) {
        say($x);
    }
}
say(2);
