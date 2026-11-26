# kind: fault
# model: t/models/hash.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my %g = (a => 1);
sub f() {
    return %g;
}
say(1);
{
    my @r = (f());
    say(scalar(@r));
}
my $x = f();
say(2);
