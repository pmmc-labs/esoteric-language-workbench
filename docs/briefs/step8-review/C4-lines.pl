use v5.42;
my $u;
sub id($p) { return $p }
sub two($p, $q) { return $p }
sub ret($p) {
  return
    $p . $u;
}
sub ret2($p) {
  return $p .
    $u;
}
sub lastv($p) {
  my $t = 1;
  $p +
    $u
}
sub dflt($p, $q = $u
  + 1) {
  return $q }
my $r = ret(1);
$r = ret2(1);
$r = lastv(1);
$r = dflt(1);
$r = id(1)
  + $u;
$r = id(1) +
  id($u + 1) +
  id(2);
my $i = 0;
while ($i < 1 &&
  id($i) + $u < 5) { $i++; }
for ($i = 0;
  $i < 1;
  $i = id($i) + 1 + $u) { }
my $k = two(1,
   id(2)) + two(
  7
);
