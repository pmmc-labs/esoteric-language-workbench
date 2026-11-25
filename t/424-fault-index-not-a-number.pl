# kind: fault
# model: t/models/list.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2, 3);
    my $i = '2';
    say($a[$i]);
}
{
    my @a = (1, 2, 3);
    my $i = 'x';
    say($a[$i]);
}
say(2);
