# kind: fault
# model: t/models/each.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2, 3);
    my @b = (7);
    for my $x (scalar(@a)) {
        say($x);
    }
}
{
    my @a = (1, 2, 3);
    my @b = (7);
    for my $x (scalar(@a)) {
        say($x);
        $a[0] = 9;
    }
}
say(2);
