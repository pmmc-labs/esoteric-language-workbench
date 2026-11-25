# kind: refused
# perl takes the variable's value for the name of a label, and leaves
# the loop L (T120).
use v5.42;
my $i = 0;
my $name = "L";
L: while ($i++ < 3) {
    last $name;
}
