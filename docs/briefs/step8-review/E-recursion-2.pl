use v5.42;
sub d($n) { return 0 if $n == 0; return 1 + d($n - 1); }
sub top($n) { return d($n) }
sub self($n, $v = $n == 0 ? 0 : self($n - 1)) { return $v + 1 }
say self(98);
say "a";
say self(99);
say "b";
sub updown($n, $again) { if ($n == 0) { return 0 } my $r = updown($n - 1, 0); $r = $r + updown($n - 1, 0) if $again; return 1; }
say updown(99, 0);
say "c";
say updown(100, 1);
