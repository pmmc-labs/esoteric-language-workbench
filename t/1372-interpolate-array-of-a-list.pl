# kind: refused
# perl prints 4.
use v5.42;
my $x = 3;
say "@{[ $x + 1 ]}";
