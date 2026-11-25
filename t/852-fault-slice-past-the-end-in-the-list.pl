# kind: fault
# model: t/models/each.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2, 3);
    for my $x (@a[0, 2]) {
        say($x);
    }
}
{
    my @a = (1, 2, 3);
    for my $x (@a[0, 3]) {
        say($x);
    }
}
say(2);
