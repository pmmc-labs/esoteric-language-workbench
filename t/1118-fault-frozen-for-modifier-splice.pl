# kind: fault
# model: t/models/it.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2, 3);
    say($_) for (@a);
}
{
    my @a = (1, 2, 3);
    splice(@a, 0, 0) for (@a);
}
say(2);
