# kind: fault
# model: t/models/sub.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
sub none() {
    return;
}
sub show($p = 'default') {
    return $p;
}
sub tail($p) {
    return $p || (+none());
}
say(1);
{
    my $v = tail(0);
    say(show(tail(4)));
}
say(show(tail(0)));
say(2);
