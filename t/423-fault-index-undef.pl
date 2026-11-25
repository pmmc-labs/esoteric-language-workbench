# kind: fault
# model: t/models/list.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2, 3);
    my $u = 1;
    say($a[$u]);
}
{
    my @a = (1, 2, 3);
    my $u;
    say($a[$u]);
}
say(2);
