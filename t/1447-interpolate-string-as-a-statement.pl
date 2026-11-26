# kind: refused
# perl warns: Useless use of string in void context.
use v5.42;
my $x = 3;
"a$x";
