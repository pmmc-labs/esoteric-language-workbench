# kind: fault
# model: t/models/var.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $v = 1;
    $v += false;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v += (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
say(2);
