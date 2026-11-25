# kind: fault
# model: t/models/var.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $v = 999999999999998.0;
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1000000000000001.0;
    $v--;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
say(2);
