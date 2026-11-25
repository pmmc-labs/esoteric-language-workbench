# kind: fault
# model: t/models/sub.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
sub ends($p) {
    {
        say('in');
    }
}
sub tail($p) {
    return $p ? 5 : ends($p);
}
say(1);
{
    say(tail(1));
    tail(0);
}
my $v = tail(0);
say(2);
