# kind: refused
# perl: r at FILE line 5 (T317).
use v5.42;
my %h = (k => 1);
sub g() {
  return $h{k} +
    die "r";
}
say g();
