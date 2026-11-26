# kind: refused
# perl leaves the loop round the map, and warns (T59).
use v5.42;
for my $i (1 .. 3) {
    my @r = map { last if $_ == 2; $_ } (1, 2, 3);
    say $i;
}
