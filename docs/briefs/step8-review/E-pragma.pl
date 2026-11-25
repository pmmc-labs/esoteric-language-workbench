use v5.42;
no warnings 'recursion';
use utf8;
use open ':std', ':encoding(UTF-8)';
sub d($n) { return 0 if $n == 0; return 1 + d($n - 1); }
say d(300);
my $u;
say "é" . 1;
say $u + 1;
say "abc" + 1;
sub f($x) { $x * 2; return 1 }
