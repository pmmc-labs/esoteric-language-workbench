# kind: fault
# model: t/models/list.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2, 3);
    say($a['2']);
}
{
    my @a = (1, 2, 3);
    say($a['x']);
}
say(2);
