# kind: fault
# model: t/models/list.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2, 3);
    splice(@a, 0, 9223372036854775807);
    say(scalar(@a));
}
{
    my @a = (1, 2, 3);
    splice(@a, 0, 1e+30);
}
say(2);
