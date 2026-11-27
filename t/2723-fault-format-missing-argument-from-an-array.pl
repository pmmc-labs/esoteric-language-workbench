# kind: fault
# perl prints 1-2- and warns: Missing argument.
use v5.42;
my @l = (1, 2);
say sprintf("%s-%s-%s", @l);
