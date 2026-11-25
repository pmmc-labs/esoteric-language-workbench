# kind: fault
# model: t/models/list.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2, 3);
    say(@a, '!');
}
{
    my @a = (1, 2, 3);
    $a[4] = 5;
    say('before', @a);
}
say(2);
