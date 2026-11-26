# kind: refused
# shift with no array shifts @_ in a sub (T152), with a signature or with none.
use v5.42;
sub head { my $x = shift; return $x; }
say head(1, 2);
