# kind: fault
# model: t/models/hash.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my %g = (a => 1, b => 2);
sub f() {
    return delete(@g{'a', 'b'});
}
say(1);
{
    my @r = (f());
    say(scalar(@r));
}
my $x = f();
say(2);
