# kind: fault
# model: t/models/it.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2, 3);
    for (@a) {
        say($_);
    }
}
{
    my @a = (1, 2, 3);
    for (@a) {
        shift(@a);
        last;
    }
}
say(2);
