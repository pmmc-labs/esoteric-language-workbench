# kind: refused
# perl does not compile it: Can't modify anonymous array ([]) in postincrement (++) near ']++'.
use v5.42;
my $x = [1]++;
