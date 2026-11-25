# kind: fault
# model: t/models/loop.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $v = '0';
    while ($v == 1) {
        say('in');
    }
    say('after');
}
{
    my $v = 'zero';
    while ($v == 1) {
        say('in');
    }
    say('after');
}
say(2);
