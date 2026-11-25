# kind: fault
# model: t/models/var.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
{
    my $v = 0;
    if ($v) {
        say(1 / $v);
    } else {
        say('else');
    }
}
{
    my $v = 0;
    if (!$v) {
        say(1 / $v);
    } else {
        say('else');
    }
}
say(2);
