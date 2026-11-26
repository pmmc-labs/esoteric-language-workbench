# kind: refused
# perl dies: Can't "last" outside a loop block (T59).
use v5.42;
for my $i (1) {
    my @r = sort { last; 0 } (3, 1, 2);
}
