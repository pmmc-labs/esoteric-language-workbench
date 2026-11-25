# kind: fault
# model: t/models/list.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1);
    say(pop(@a) + 1);
}
{
    my @a = (1);
    pop(@a);
    say(pop(@a) + 1);
}
say(2);
