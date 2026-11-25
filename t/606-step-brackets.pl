# kind: refused
# perl takes it: the brackets change nothing there. A step is hard
# against its variable here.
use v5.42;
my $x = 1;
my $y = ($x)++;
