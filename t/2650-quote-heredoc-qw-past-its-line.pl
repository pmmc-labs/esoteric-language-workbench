# kind: refused
# perl does not compile it: Can't find string terminator ")" anywhere before EOF.
use v5.42;
my @l = (<<EOT, qw(a
b));
c
EOT
say scalar(@l);
