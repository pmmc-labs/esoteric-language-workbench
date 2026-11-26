# kind: refused
# perl: 123; the last leaves the modifier's own loop (T191).
use v5.42;
for my $i (1 .. 3) {
    last for 1, 2;
    print $i;
}
