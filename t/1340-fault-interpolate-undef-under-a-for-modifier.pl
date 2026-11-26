# kind: fault
# model: t/models/interp.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2);
    say("<$_>") for (@a);
}
{
    my @a = (1, (undef));
    say("<$_>") for (@a);
}
say(2);
