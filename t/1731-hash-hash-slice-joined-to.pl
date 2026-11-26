# kind: refused
# perl takes it, and prints nothing.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
@h{"a", "b"} .= "x";
