# kind: fault
# model: t/models/each.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2, 3);
    my $x2 = 0;
    for my $x (@a) {
        say($x);
    }
}
{
    my @a = (1, 2, 3);
    my $x2 = 0;
    for my $x (@a) {
        say($x);
        ($x2, @a) = (5, 6);
        last;
    }
}
say(2);
