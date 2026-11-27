# kind: refused
# perl: a at FILE line 5, the second line (T317).
use v5.42;
my %h = (k => 1);
$h{k} =
  die "a";
