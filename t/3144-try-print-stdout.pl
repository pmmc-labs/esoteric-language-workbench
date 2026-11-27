# kind: refused
# perl prints x; STDERR is the one handle.
use v5.42;
print STDOUT "x
";
