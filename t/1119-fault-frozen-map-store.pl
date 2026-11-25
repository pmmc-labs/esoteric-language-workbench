# kind: fault
# model: t/models/it.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2, 3);
    my @r = ((map { $_ + 0 } (@a)));
}
{
    my @a = (1, 2, 3);
    my @r = ((map { $a[0] = 9; $_ + 0 } (@a)));
}
say(2);
