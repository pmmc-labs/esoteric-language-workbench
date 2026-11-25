# kind: refused
# perl: 095 (T185).
use v5.42;
my $v = 5;
sub bump() {
    $v = 9;
    return 5;
}
my @r = (reverse($v, 0), bump());
say @r;
