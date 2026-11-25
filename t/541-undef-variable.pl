# kind: fault
# model: t/models/var.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $v;
    say($v // 'undef');
}
{
    my $v;
    say($v);
}
say(2);
