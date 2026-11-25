# kind: fault
# model: t/models/var.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $v = 1;
    say(10 / ($v = 5));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say($v / ($v = 0));
}
say(2);
