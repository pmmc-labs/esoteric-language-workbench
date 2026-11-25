# kind: refused
# perl tests the last part alone, and warns: Useless use of numeric lt
# (<) in void context (T122, D60).
use v5.42;
my $i = 0;
my $j = 9;
for (; $i < 3, $j > 7; $i++, $j--) {
    say $i;
}
