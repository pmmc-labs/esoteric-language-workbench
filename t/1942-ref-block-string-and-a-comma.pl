# kind: refused
# perl runs it ('') and warns: Useless use of anonymous hash ({}) in void context.
use v5.42;
my $x = 1;
{ "$x", 1 }
