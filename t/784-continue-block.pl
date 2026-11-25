# kind: refused
# perl runs it after each time round the block. Cut.
use v5.42;
my $i = 0;
while ($i < 3) {
    $i++;
} continue {
    print "c";
}
