### store-in-closure
my @a = (1, 2); my @s;
for my $x (@a) { push @s, sub { $x = 5 } }
$s[0]->(); say "@a";
### inc-in-closure
my @a = (1, 2); my @s;
for my $x (@a) { push @s, sub { $x++ } }
$s[0]->(); $s[0]->(); say "@a";
### append-in-closure
my @a = ("a", "b"); my @s;
for my $x (@a) { push @s, sub { $x .= "!" } }
$s[1]->(); say "@a";
### store-in-closure-during-loop
my @a = (1, 2);
for my $x (@a) { my $f = sub { $x = 7 }; $f->(); }
say "@a";
### viv-in-closure
my @a = (undef, undef); my @s;
for my $x (@a) { push @s, sub { $x->[0] = 1 } }
$s[0]->(); say join ",", map { ref($_) || "plain" } @a;
### viv-push-in-closure
my @a = (undef); my @s;
for my $x (@a) { push @s, sub { push $x->@*, 1 } }
$s[0]->(); say ref($a[0]) || "plain";
### viv-in-closure-hash-values
my %h = (k => undef); my @s;
for my $v (values %h) { push @s, sub { $v->{z} = 1 } }
$s[0]->(); say ref($h{k}) || "plain";
### two-closures-share-loopvar
my @a = (1); my ($get, $set);
for my $x (@a) { $get = sub { $x }; $set = sub { $x = 4 } }
$set->(); say $get->(), " ", $a[0];
### scalar-ternary
my ($p, $q, $c) = (1, 2, 1); my @s;
for my $x ($c ? $p : $q) { push @s, sub { $x } }
$p = 9; say $s[0]->();
### scalar-or
my ($p, $q) = (1, 2); my @s;
for my $x ($p || $q) { push @s, sub { $x } }
$p = 9; say $s[0]->();
### scalar-and
my ($p, $q) = (1, 2); my @s;
for my $x ($p && $q) { push @s, sub { $x } }
$q = 9; say $s[0]->();
### scalar-defor
my ($p, $q) = (1, 2); my @s;
for my $x ($p // $q) { push @s, sub { $x } }
$p = 9; say $s[0]->();
### scalar-brackets
my $p = 1; my @s;
for my $x (($p)) { push @s, sub { $x } }
$p = 9; say $s[0]->();
### scalar-plus
my $p = 1; my @s;
for my $x (+$p) { push @s, sub { $x } }
$p = 9; say $s[0]->();
### scalar-assign
my $p = 1; my @s;
for my $x ($p = 3) { push @s, sub { $x } }
$p = 9; say $s[0]->();
### scalar-preinc
my $p = 1; my @s;
for my $x (++$p) { push @s, sub { $x } }
$p = 9; say $s[0]->();
### scalar-postinc
my $p = 1; my @s;
for my $x ($p++) { push @s, sub { $x } }
$p = 9; say $s[0]->();
### scalar-grep
my ($p, $q) = (1, 2); my @s;
for my $x (grep { 1 } $p, $q) { push @s, sub { $x } }
$p = 9; say $s[0]->();
### scalar-sort
my ($p, $q) = (1, 2); my @s;
for my $x (sort { $a <=> $b } $p, $q) { push @s, sub { $x } }
$p = 9; say $s[0]->();
### scalar-sort-plain
my ($p, $q) = ("a", "b"); my @s;
for my $x (sort $p, $q) { push @s, sub { $x } }
$p = "z"; say $s[0]->();
### scalar-reverse
my ($p, $q) = (1, 2); my @s;
for my $x (reverse $p, $q) { push @s, sub { $x } }
$q = 9; say $s[0]->();
### scalar-map
my ($p, $q) = (1, 2); my @s;
for my $x (map { $_ } $p, $q) { push @s, sub { $x } }
$p = 9; say $s[0]->();
### scalar-listslice
my ($p, $q) = (1, 2); my @s;
for my $x (($p, $q)[0]) { push @s, sub { $x } }
$p = 9; say $s[0]->();
### scalar-deref
my $p = 1; my $r = \$p; my @s;
for my $x ($r->$*) { push @s, sub { $x } }
$p = 9; say $s[0]->();
### scalar-deref-braces
my $p = 1; my $r = \$p; my @s;
for my $x (${ $r }) { push @s, sub { $x } }
$p = 9; say $s[0]->();
### scalar-repeat
my $p = 1; my @s;
for my $x (($p) x 2) { push @s, sub { $x } }
$p = 9; say $s[0]->();
### scalar-join
my $p = 1; my @s;
for my $x (join "", $p) { push @s, sub { $x } }
$p = 9; say $s[0]->();
### scalar-call-ret
my $p = 1; my @s;
sub f() { return $p }
for my $x (f()) { push @s, sub { $x } }
$p = 9; say $s[0]->();
### scalar-call-last
my $p = 1; my @s;
sub g() { $p }
for my $x (g()) { push @s, sub { $x } }
$p = 9; say $s[0]->();
### array-call-ret
my @a = (1, 2); my @s;
sub h() { return @a }
for my $x (h()) { push @s, sub { $x } }
$a[0] = 9; say $s[0]->();
### array-call-last
my @a = (1, 2); my @s;
sub h2() { @a }
for my $x (h2()) { push @s, sub { $x } }
$a[0] = 9; say $s[0]->();
### array-grep-then-store
my @a = (1, 2); my @s;
for my $x (grep { 1 } @a) { push @s, sub { $x } }
$a[0] = 9; say $s[0]->();
### array-sort
my @a = (2, 1); my @s;
for my $x (sort { $a <=> $b } @a) { push @s, sub { $x } }
$a[1] = 9; say $s[0]->();
### array-reverse
my @a = (1, 2); my @s;
for my $x (reverse @a) { push @s, sub { $x } }
$a[1] = 9; say $s[0]->();
### array-map
my @a = (1, 2); my @s;
for my $x (map { $_ } @a) { push @s, sub { $x } }
$a[0] = 9; say $s[0]->();
### literal-constants
my @s;
for my $x (1, 2) { push @s, sub { $x } }
say $s[0]->();
### literal-store-in-closure
my @s;
for my $x (1, 2) { push @s, sub { $x = 5 } }
$s[0]->(); say "ok";
### range-store-in-closure
my @s;
for my $x (1 .. 2) { push @s, sub { $x = 5; $x } }
say $s[0]->(), $s[0]->();
### keys-store
my %h = (a => 1); my @s;
for my $k (keys %h) { push @s, sub { $k = "z" } }
$s[0]->(); say join ",", keys %h;
### call-ret-store
my @a = (1); my @s;
sub h3() { return @a }
for my $x (h3()) { push @s, sub { $x = 5; $x } }
say $s[0]->(), $a[0];
### nested-closure-store
my @a = (1); my @s;
for my $x (@a) { push @s, sub { return sub { $x = 6 } } }
$s[0]->()->(); say $a[0];
### map-block-closure
my @a = (1, 2); my @s;
for my $x (@a) { push @s, map { sub { $x } } 1 }
$a[0] = 9; say $s[0]->();
### hash-elem-store-in-closure
my %h = (a => 1); my @s;
for my $x ($h{a}) { push @s, sub { $x = 3 } }
$s[0]->(); say $h{a};
### array-elem-store-in-closure
my @a = (1); my @s;
for my $x ($a[0]) { push @s, sub { $x = 3 } }
$s[0]->(); say $a[0];
### slice-store-in-closure
my @a = (1, 2); my @s;
for my $x (@a[0, 1]) { push @s, sub { $x = 3 } }
$s[1]->(); say "@a";
### chain-store-in-closure
my $r = [1, 2]; my @s;
for my $x ($r->@*) { push @s, sub { $x = 3 } }
$s[0]->(); say "@$r";
### scalar-map-block-returns-var
my $p = 1; my @s;
for my $x (map { $p } 1) { push @s, sub { $x } }
$p = 9; say $s[0]->();
### scalar-closure-call
my $p = 1; my $f = sub { $p }; my @s;
for my $x ($f->()) { push @s, sub { $x } }
$p = 9; say $s[0]->();
### scalar-scalar-fn
my $p = 1; my @s;
for my $x (scalar($p)) { push @s, sub { $x } }
$p = 9; say $s[0]->();
### scalar-interp
my $p = 1; my @s;
for my $x ("$p") { push @s, sub { $x } }
$p = 9; say $s[0]->();
### scalar-param
sub mk($p) { my @s; for my $x ($p) { push @s, sub { $x } } $p = 9; return $s[0]->() }
say mk(1);
### scalar-captured-by-other-closure-changes
my $p = 1; my $set = sub { $p = 9 }; my @s;
for my $x (grep { 1 } $p) { push @s, sub { $x } }
$set->(); say $s[0]->();
### lastindex-alias
my @a = (1); my @s;
for my $x ($#a) { push @s, sub { $x } }
say $s[0]->();
### nested-loop-inner-over-outer-var
my @a = (1, 2); my @s;
for my $x (@a) { for my $y (grep { 1 } $x) { push @s, sub { $y } } }
$a[0] = 9; say $s[0]->();
### hash-in-list-values-alias
my %h = (k => 1); my @s;
for my $x (%h) { push @s, sub { $x } }
$h{k} = 9; say join ",", sort map { $_->() } @s;
### range-ends-var
my $n = 2; my @s;
for my $x (1 .. $n) { push @s, sub { $x } }
$n = 9; say join ",", map { $_->() } @s;
