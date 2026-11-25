# kind: fault
# model: t/models/var.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $v;
    say(($v || 0) + 1);
}
{
    my $v;
    say($v + 1);
}
say(2);
