# kind: fault
# model: t/models/var.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $v = (undef);
    $v -= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (undef);
    $v /= 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
say(2);
