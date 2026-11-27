# model: t/models/die.py
use v5.42;
{ my @a = (7, 26, 16, 24, 23); my $n = 0;
try { my @m = map { $n++; die "map $_\n" if $_ == 16; $_ * 2 } @a; say "@m" } catch ($e) { print $e }
try { my @g = grep { die "grep $_\n" if $_ == 16; $_ % 2 } @a; say "@g" } catch ($e) { print $e }
try { my @s = sort { die "sort\n" if $a == 16 || $b == 16; $a <=> $b } @a; say "@s" } catch ($e) { print $e }
my @s = sort { $a <=> $b } @a; push @a, 0; say "$n @s ", scalar(@a); }
{ my @a = (10, 27, 9); my $n = 0;
try { my @m = map { $n++; die "map $_\n" if $_ == 9; $_ * 2 } @a; say "@m" } catch ($e) { print $e }
try { my @g = grep { die "grep $_\n" if $_ == 9; $_ % 2 } @a; say "@g" } catch ($e) { print $e }
try { my @s = sort { die "sort\n" if $a == 9 || $b == 9; $a <=> $b } @a; say "@s" } catch ($e) { print $e }
my @s = sort { $a <=> $b } @a; push @a, 0; say "$n @s ", scalar(@a); }
{ my @a = (4, 23, 18, 29); my $n = 0;
try { my @m = map { $n++; die "map $_\n" if $_ == 23; $_ * 2 } @a; say "@m" } catch ($e) { print $e }
try { my @g = grep { die "grep $_\n" if $_ == 23; $_ % 2 } @a; say "@g" } catch ($e) { print $e }
try { my @s = sort { die "sort\n" if $a == 23 || $b == 23; $a <=> $b } @a; say "@s" } catch ($e) { print $e }
my @s = sort { $a <=> $b } @a; push @a, 0; say "$n @s ", scalar(@a); }
{ my @a = (10, 15, 27, 13, 20); my $n = 0;
try { my @m = map { $n++; die "map $_\n" if $_ == 20; $_ * 2 } @a; say "@m" } catch ($e) { print $e }
try { my @g = grep { die "grep $_\n" if $_ == 20; $_ % 2 } @a; say "@g" } catch ($e) { print $e }
try { my @s = sort { die "sort\n" if $a == 20 || $b == 20; $a <=> $b } @a; say "@s" } catch ($e) { print $e }
my @s = sort { $a <=> $b } @a; push @a, 0; say "$n @s ", scalar(@a); }
{ my @a = (28, 15, 22, 27, 16, 12, 11); my $n = 0;
try { my @m = map { $n++; die "map $_\n" if $_ == 16; $_ * 2 } @a; say "@m" } catch ($e) { print $e }
try { my @g = grep { die "grep $_\n" if $_ == 16; $_ % 2 } @a; say "@g" } catch ($e) { print $e }
try { my @s = sort { die "sort\n" if $a == 16 || $b == 16; $a <=> $b } @a; say "@s" } catch ($e) { print $e }
my @s = sort { $a <=> $b } @a; push @a, 0; say "$n @s ", scalar(@a); }
{ my @a = (14, 25, 15, 13, 9, 5, 3, 6); my $n = 0;
try { my @m = map { $n++; die "map $_\n" if $_ == 9; $_ * 2 } @a; say "@m" } catch ($e) { print $e }
try { my @g = grep { die "grep $_\n" if $_ == 9; $_ % 2 } @a; say "@g" } catch ($e) { print $e }
try { my @s = sort { die "sort\n" if $a == 9 || $b == 9; $a <=> $b } @a; say "@s" } catch ($e) { print $e }
my @s = sort { $a <=> $b } @a; push @a, 0; say "$n @s ", scalar(@a); }
{ my @a = (3, 1, 2);
my @m = map { my $v = $_; try { die "odd\n" if $v % 2 } catch ($e) { $v = 0 } $v } @a; say "@m";
my @s = sort { my $c = 0; try { die "x\n" if $a == 2; $c = $a <=> $b } catch ($e) { $c = $b <=> $a } $c } @a; say scalar(@s); }
