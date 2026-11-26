# kind: fault
# model: t/models/interp.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2, 3);
    for my $v ("$a[2]") {
        say($v);
    }
}
{
    my @a = (1, 2, 3);
    for my $v ("$a[3]") {
        say($v);
    }
}
say(2);
