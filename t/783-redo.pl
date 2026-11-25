# kind: refused
# perl runs the block again without testing. Cut.
use v5.42;
my $i = 0;
while ($i < 3) {
    $i++;
    redo if $i == 1;
}
