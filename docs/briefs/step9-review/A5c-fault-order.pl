use v5.42;
# perl refuses the target before the right side runs.
my @a = (1);
sub p($v) { say $v; return $v }
$a[-9] += p(5);
