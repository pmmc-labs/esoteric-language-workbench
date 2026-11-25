use v5.42;
sub a($x, $c) { $x * 2 if $c }
sub b($x, $c) { $x++ if $c }
sub c($x, $c) { $x = 7 unless $c }
sub d($x, $c) { a($x, 1) if $c }
say "[" . a(4, 1) . "]";
say "[" . a(4, 0) . "]";
say "[" . a(4, "") . "]";
say "[" . b(4, 0) . "]";
say "[" . c(4, 3) . "]";
say "[" . d(4, 0) . "]";
a(1, 1); a(1, 0);
