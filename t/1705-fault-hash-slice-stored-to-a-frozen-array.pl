# kind: fault
# model: t/models/hash.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2);
    for my $v (@a) {
        say($v);
        last;
    }
}
{
    my @a = (1, 2);
    for my $v (@a) {
        @a[0, 1] = (5, 6);
        last;
    }
}
say(2);
