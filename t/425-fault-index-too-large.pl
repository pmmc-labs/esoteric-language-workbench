# kind: fault
# model: t/models/list.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my @a = (1, 2, 3);
    say(defined($a[9223372036854775807]) ? (('[' . $a[9223372036854775807]) . ']') : 'undef');
}
{
    my @a = (1, 2, 3);
    say(defined($a[1e+30]) ? (('[' . $a[1e+30]) . ']') : 'undef');
}
say(2);
