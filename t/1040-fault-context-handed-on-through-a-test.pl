# kind: fault
# model: t/models/ret.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my @a = (4, 5, 6);
sub f() {
    return (1, 2);
}
sub g($p) {
    return $p ? f() : 0;
}
say(1);
{
    say(g(1));
    my $y = g(0);
}
my $x = g(1);
say(2);
