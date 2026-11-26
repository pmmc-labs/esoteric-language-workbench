# kind: fault
# model: t/models/interp.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2, 3);
    my @b = (7);
    for my $v ("@a", @b) {
        push(@a, 4);
        say($v);
    }
}
{
    my @a = (1, 2, 3);
    my @b = (7);
    for my $v ("@a", @b) {
        push(@b, 4);
        last;
    }
}
say(2);
