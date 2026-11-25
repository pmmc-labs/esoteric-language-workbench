use v5.42;
sub d($n) { return 0 if $n == 0; return 1 + d($n - 1); }
say d(98);
say d(98);
my $i = 0;
while ($i++ < 3) { d(98); }
say "quiet so far";
sub e($n, $v = e2($n)) { return $v }
sub e2($n) { return $n == 0 ? 0 : e($n - 1) }
say e(60);
say e(98);
say "then";
say e(99);
