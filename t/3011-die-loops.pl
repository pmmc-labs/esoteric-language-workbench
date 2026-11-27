# model: t/models/die.py
use v5.42;
{ my @a = (9, 3, 3); my $seen = 0;
try { for my $x (@a) { $seen++; die "stop at $x\n" if $x == 9 } say "ran all" } catch ($e) { print $e }
push @a, 0; $a[0] = 0; say "$seen @a"; }
{ my @a = (7, 9, 5, 2); my $seen = 0;
try { for my $x (@a) { $seen++; die "stop at $x\n" if $x == 7 } say "ran all" } catch ($e) { print $e }
push @a, 1; $a[0] = 0; say "$seen @a"; }
{ my @a = (5, 8, 4, 4); my $seen = 0;
try { for my $x (@a) { $seen++; die "stop at $x\n" if $x == 5 } say "ran all" } catch ($e) { print $e }
push @a, 2; $a[0] = 0; say "$seen @a"; }
{ my @a = (9, 9, 6, 5, 7, 7); my $seen = 0;
try { for my $x (@a) { $seen++; die "stop at $x\n" if $x == 7 } say "ran all" } catch ($e) { print $e }
push @a, 3; $a[0] = 0; say "$seen @a"; }
{ my @a = (8, 1, 3, 4, 1); my $seen = 0;
try { for my $x (@a) { $seen++; die "stop at $x\n" if $x == 1 } say "ran all" } catch ($e) { print $e }
push @a, 4; $a[0] = 0; say "$seen @a"; }
{ my @a = (5, 3, 3); my $seen = 0;
try { for my $x (@a) { $seen++; die "stop at $x\n" if $x == 100 } say "ran all" } catch ($e) { print $e }
push @a, 5; $a[0] = 0; say "$seen @a"; }
{ my @a = (3, 5, 4, 7, 4); my $seen = 0;
try { for my $x (@a) { $seen++; die "stop at $x\n" if $x == 4 } say "ran all" } catch ($e) { print $e }
push @a, 6; $a[0] = 0; say "$seen @a"; }
{ my @a = (4, 9, 5, 9); my $seen = 0;
try { for my $x (@a) { $seen++; die "stop at $x\n" if $x == 4 } say "ran all" } catch ($e) { print $e }
push @a, 7; $a[0] = 0; say "$seen @a"; }
{ my %h = (a => 1, b => 2, c => 3);
try { for my $v (sort { $a <=> $b } values %h) { die "v $v\n" if $v == 2 } } catch ($e) { print $e }
try { for my $k (sort keys %h) { die "k $k\n" if $h{$k} == 3 } } catch ($e) { print $e }
try { for my $v (sort { $a <=> $b } values %h) { die "plain\n" } } catch ($e) { print $e }
$h{d} = 4; delete $h{a}; say join(",", sort keys %h); }
{ my @o = (1, 2, 3); my @i = (4, 5);
for my $x (@o) { try { for my $y (@i) { die "$x$y\n" if $y == 5 } } catch ($e) { print $e; push @i, 6 if $x == 2 } }
say "@i"; }
