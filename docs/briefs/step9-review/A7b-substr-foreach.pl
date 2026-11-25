use v5.42;
my $s = "abc";
for my $x (substr($s, 0, 1)) { $s = "zzz"; say $x; }
my $p = 1;
for my $x ($p = 5, $p += 1, ++$p, $p++) { say $x; $p = 100; }
