# kind: fault
# model: t/models/list.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2, 3);
    my @s = (@a[0, '1']);
    say(scalar(@s));
}
{
    my @a = (1, 2, 3);
    my @s = (@a[0, 'one']);
}
say(2);
