# kind: refused
# perl runs it, and says nothing.
use v5.42;
my $r;
for my $v ($r, 1) {
    $r->{k} = 1;
}
