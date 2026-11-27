# kind: dies
# From a sub a hundred and more calls deep.
use v5.42;
no warnings 'recursion';
sub down($n) { die "bottom $n" if $n == 150; return down($n + 1) }
say "going down";
down(0);
