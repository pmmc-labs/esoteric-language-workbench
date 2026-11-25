# kind: fault
# model: t/models/var.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $v = '0';
    if ($v == 0) {
        say('zero');
    }
}
{
    my $v = 'zero';
    if ($v == 0) {
        say('zero');
    }
}
say(2);
