# kind: fault
# model: t/models/ret.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
sub loud() {
    say('worked out');
    return 1;
}
sub f() {
    return (loud(), 2);
}
say(1);
say(f());
my $x = f();
say(2);
