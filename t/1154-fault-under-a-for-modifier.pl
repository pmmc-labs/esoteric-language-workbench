# kind: fault
# model: t/models/it.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2, 3);
    my $t = 0;
    $t += (6 / $_) for (@a);
}
{
    my @a = (1, 2, 3);
    my $t = 0;
    $t += (6 / ($_ - 3)) for (@a);
}
say(2);
