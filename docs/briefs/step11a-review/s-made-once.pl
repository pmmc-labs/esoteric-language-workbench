use v5.42;
no warnings 'recursion';
my @a = (1, 2, 3);
sub f($x) { return "<$x>" }
sub f2($x) { "<$x>" }
sub f3($x) { return ("<$x>", "[$x]") }
sub f4($x) { return grep { true } "<$x>" }
sub f5($x) { reverse("<$x>", "k") }
sub f6($x) { return $x ? "<$x>" : "z$x" }
sub f7($x) { return "$x" }
sub f8($x) { return ("@a", "$a[$x]", "$#a") }
sub h($n) { return ("<$n>", $n > 0 ? h($n - 1) : ()) }
my @r;
@r = (f(1), f(2)); say "01 @r";
@r = (f2(1), f2(2)); say "02 @r";
@r = (f3(1), f3(2)); say "03 @r";
@r = (f4(1), f4(2)); say "04 @r";
@r = (f5(1), f5(2)); say "05 @r";
@r = (f6(1), f6(0), f6(2)); say "06 @r";
@r = (f7(1), f7(2)); say "07 @r";
@r = (f8(0), push(@a, 4), f8(1)); say "08 @r";
@r = h(3); say "09 @r";
@r = (h(1), h(2)); say "10 @r";
@r = map { grep { true } "<$_>" } 1, 2, 3; say "11 @r";
@r = map { reverse("<$_>", "k") } 1, 2; say "12 @r";
@r = map { sort("<$_>", "a") } 1, 2; say "13 @r";
@r = grep { true } map { "<$_>" } 1, 2; say "14 @r";
@r = reverse(map { "<$_>" } 1, 2); say "15 @r";
@r = sort { $b cmp $a } map { "<$_>" } 1, 2; say "16 @r";
@r = map { ("<$_>") x 2 } 1, 2; say "17 @r";
@r = map { $_ > 1 ? "<$_>" : "z$_" } 1, 2, 3; say "18 @r";
@r = map { "$_" } 1, 2; say "19 @r";
@r = map { ("$_", "${_}") } 1, 2; say "20 @r";
@r = map { f($_) } 1, 2; say "21 @r";
@r = map { f4($_) } 1, 2; say "22 @r";
say "23 ", join(",", f(1), f(2), f4(3), f4(4), f5(5), f5(6));
say "24 ", f(1), f(2), f4(3), f4(4);
say "25 ", f(1) . f(2) . f(1);
say "26 ", f(f(f(1)) . f(2));
@r = (f4(1))[0] . (f4(2))[0]; say "27 @r";
for my $v (f4(1), f4(2), f(3), f(4)) { push @r, $v; } say "28 @r";
for my $v (map { "<$_>" } 1, 2) { push @r, $v; } say "29 @r";
my ($p, $q) = (f4(1), f4(2)); say "30 $p $q";
sub two($p, $q) { return "$p$q" }
say "31 ", two(f4(1), f4(2)), two(f(1), f(2)), two(f5(1));
@r = (map { "<$_>" } 1, 2)[1, 0]; say "32 @r";
@r = map { my $k = $_; map { "$k$_" } 1, 2 } 1, 2; say "33 @r";
@r = map { my $k = $_; grep { true } map { "$k$_" } 1, 2 } 1, 2; say "34 @r";
@r = sort { $a cmp $b } (f4(2), f4(1)); say "35 @r";
@r = reverse(f4(1), f4(2)); say "36 @r";
@r = grep { true } (f4(1), f4(2), f(3), f(4)); say "37 @r";
@r = ((grep { true } "$a[0]", "$a[1]"), ($a[0] = 9)); say "38 @r";
