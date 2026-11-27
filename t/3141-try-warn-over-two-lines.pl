# kind: refused
# perl names a line of its own choosing (T317).
use v5.42;
my %h = (k => 1);
my $x = $h{k} +
  warn "w";
