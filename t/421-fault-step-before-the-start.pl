# kind: fault
# model: t/models/list.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2, 3);
    $a[(-3)]++;
    say(defined($a[(-4)]) ? (('[' . $a[(-4)]) . ']') : 'undef');
}
{
    my @a = (1, 2, 3);
    $a[(-4)]++;
}
say(2);
