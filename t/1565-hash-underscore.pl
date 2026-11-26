# kind: refused
# perl does not compile it: Can't use global %_ in "my".
use v5.42;
my %_ = (a => 1);
