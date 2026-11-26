# kind: refused
# perl: 13; k is the comparator, and the list is 3, 1 (T189, T29).
use v5.42;
sub k() {
    return 5;
}
my @r = sort k(), 3, 1;
say @r;
