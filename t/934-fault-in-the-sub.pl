# kind: fault
# model: t/models/sub.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
sub div($p) {
    my $x = 10;
    say('in');
    return $x / $p;
}
say(1);
say(div(5));
say(div(0));
say(2);
