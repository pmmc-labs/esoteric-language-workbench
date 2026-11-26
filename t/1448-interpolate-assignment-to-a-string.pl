# kind: refused
# perl does not compile it: Can't modify string in scalar assignment.
use v5.42;
my $x = 3;
"$x" = 5;
