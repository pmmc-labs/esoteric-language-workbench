# kind: fault
# model: t/models/var.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $v = 0;
    say(1 / $v) if $v;
    say('after');
}
{
    my $v = 0;
    say(1 / $v) unless $v;
    say('after');
}
say(2);
