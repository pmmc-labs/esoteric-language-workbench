# kind: refused
# perl runs it, and says nothing.
use v5.42;
my $cfg;
sub get() {
    $cfg->{x} = 1;
    return 0;
}
my @l = ($cfg, get());
