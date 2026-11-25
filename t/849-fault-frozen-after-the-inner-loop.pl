# kind: fault
# model: t/models/each.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2, 3);
    for my $x (@a) {
        for my $y (@a) {
            say($y);
        }
    }
}
{
    my @a = (1, 2, 3);
    for my $x (@a) {
        for my $y (@a) {
            say($y);
        }
        $a[0] = 9;
    }
}
say(2);
