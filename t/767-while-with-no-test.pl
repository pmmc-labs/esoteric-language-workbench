# kind: refused
# An empty test is true, to perl, for while: this runs until the last.
# until () doesn't compile (T123).
use v5.42;
my $i = 0;
while () {
    last if $i++ > 2;
}
