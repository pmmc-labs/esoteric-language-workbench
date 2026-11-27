# t/models/strfn.py 2801
use v5.42;
use utf8;
use open ':std', ':encoding(UTF-8)';
{ my $s = "ab\n"; chomp($s); my $t = "ab\n"; chop $t; say "[$s|$t]"; }
{ my $s = "ab\n\n"; chomp($s); my $t = "ab\n\n"; chop $t; say "[$s|$t]"; }
{ my $s = "ab"; chomp($s); my $t = "ab"; chop $t; say "[$s|$t]"; }
{ my $s = ""; chomp($s); my $t = ""; chop $t; say "[$s|$t]"; }
{ my $s = "\n"; chomp($s); my $t = "\n"; chop $t; say "[$s|$t]"; }
{ my $s = "a\r\n"; chomp($s); my $t = "a\r\n"; chop $t; say "[$s|$t]"; }
{ my $s = "é\n"; chomp($s); my $t = "é\n"; chop $t; say "[$s|$t]"; }
{ my $s = "☺"; chomp($s); my $t = "☺"; chop $t; say "[$s|$t]"; }
{ my $s = "x\ny"; chomp($s); my $t = "x\ny"; chop $t; say "[$s|$t]"; }
{ my $s = "\n\n"; chomp($s); my $t = "\n\n"; chop $t; say "[$s|$t]"; }
{ my $x = 1 / 3; chomp($x); say $x * 3; }
{ my $x = 0.1 + 0.2; chomp $x; say $x - 0.3; }
{ my $n = 42; chomp($n); say $n + 1; }
{ my $t = true; chomp($t); say $t + 1; }
{ my $x = 1.5; chop($x); say $x, "|", $x + 1; }
{ my $n = 42; chop $n; say $n; }
{ my $s = "abc"; chop $s; chop $s; chop $s; chop $s; say "[$s]"; }
{ my $s = "line\n"; chomp $s if 1; say "[$s]"; }
{ my $s = "a\n"; chomp $s unless 0; say "[$s]"; }
{ my @l = ("x\n", "y\n"); my @r; for my $e (@l) { my $c = $e; chomp $c; push @r, $c; } say join("|", @r); }
sub trimmed($line) { chomp $line; return $line } say "[", trimmed("in a sub\n"), "]";
{ my $s = "abc\n"; chomp($s); chop($s); say length $s, $s; }
