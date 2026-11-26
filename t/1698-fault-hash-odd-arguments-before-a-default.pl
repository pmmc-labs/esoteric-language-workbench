# kind: fault
# model: t/models/hash.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
sub told() {
    say('the default ran');
    return 5;
}
sub dflt($x //= told(), %o) {
    return $x + scalar(keys(%o));
}
say(1);
say(dflt(1, 2, 3));
say(dflt((undef), 'k'));
say(2);
