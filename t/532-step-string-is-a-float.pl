# kind: fault
# model: t/models/var.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $v = 5;
    $v++;
    $v += 10000000000000000;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = '5';
    $v++;
    $v += 10000000000000000;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
say(2);
