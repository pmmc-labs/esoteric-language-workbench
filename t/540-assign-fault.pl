# kind: fault
# model: t/models/var.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $v = '12';
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 'abc';
    $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
say(2);
