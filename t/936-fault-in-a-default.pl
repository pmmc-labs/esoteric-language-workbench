# kind: fault
# model: t/models/sub.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
sub dflt($p, $q = 10 / $p) {
    return $q;
}
say(1);
{
    say(dflt(5));
    say(dflt(0, 1));
}
say(dflt(0));
say(2);
