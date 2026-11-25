# kind: fault
# model: t/models/var.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $v = (-9223372036854775807);
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = (-9223372036854775807 - 1);
    --$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
say(2);
