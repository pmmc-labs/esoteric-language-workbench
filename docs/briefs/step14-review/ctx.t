### last-stmt-array-scalar
my @a = (4, 5, 6); my $f = sub { @a }; my $c = $f->(); say $c;
### last-stmt-list-scalar
my $f = sub { (4, 5, 6) }; my $c = $f->(); say $c;
### return-nothing-scalar
my $f = sub { return }; my $c = $f->(); say defined $c ? "def" : "undef";
### return-nothing-list
my $f = sub { return }; my @l = ($f->(), 1); say scalar(@l);
### empty-body
my $f = sub { }; my @l = ($f->()); my $c = $f->(); say scalar(@l), defined $c ? "def" : "undef";
### if-last-scalar
my $f = sub ($x) { if ($x) { "yes" } }; my $c = $f->(0); say "[$c]";
### say-last
my $f = sub { say "hi" }; my $c = $f->(); say $c;
### loop-last
my $f = sub { for my $i (1..2) { } }; my @l = $f->(); say scalar(@l);
### bool-test
my $f = sub { return (0, 0) }; say $f->() ? "t" : "f";
### bool-test-arr
my @e = (); my $f = sub { return @e }; say $f->() ? "t" : "f";
### index
my @a = (10, 20, 30); my $f = sub { return (2, 0) }; say $a[$f->()];
### hash-value
my $f = sub { return (1, 2) }; my $r = { k => $f->() }; say join ",", sort keys $r->%*;
### ternary-list
my $f = sub { return (1, 2) }; my @l = (1 ? $f->() : 0); say scalar(@l);
### or-scalar
my $f = sub { return (0, 7) }; my $c = $f->() || 9; say $c;
### defor-scalar
my $f = sub { return (undef) x 2 }; my $c = $f->() // 9; say $c;
### repeat-left
my $f = sub { return (1, 2) }; say $f->() x 2;
### repeat-right
my $f = sub { return (1, 3) }; say "a" x $f->();
### list-repeat
my $f = sub { return (1, 2) }; my @l = ($f->()) x 2; say "@l";
### push
my @a; my $f = sub { return (1, 2) }; push @a, $f->(); say scalar(@a);
### scalar-of
my $f = sub { return (1, 2, 3) }; say scalar($f->());
### countof
my $f = sub { return (1, 2, 3) }; my $n = () = $f->(); say $n;
### my-list
my $f = sub { return (1, 2, 3) }; my ($x) = $f->(); say $x;
### return-through
my $f = sub { return (5, 6) }; sub g() { return $f->() } my $c = g(); my @l = g(); say $c, scalar(@l);
### last-stmt-through
my $f = sub { return (5, 6) }; sub g2() { $f->() } my $c = g2(); say $c;
### concat
my $f = sub { return (1, 2) }; say "x" . $f->();
### arith
my $f = sub { return (1, 2) }; say 10 + $f->();
### compare
my $f = sub { return (1, 2) }; say $f->() == 2 ? "eq" : "ne";
### not
my $f = sub { return (1, 0) }; say !$f->() ? "t" : "f";
### arg-of-length
my $f = sub { return ("ab", "cde") }; say length $f->();
### sort-block-uses
my $f = sub ($p, $q) { return ($q, $p) }; my @l = sort { $f->($a, $b) } 1, 2, 3; say "@l";
### in-interp-not
my $f = sub { 1 }; say "@{[ $f->() ]}";
### return-scalar-reverse
my $f = sub { return reverse("ab", "c") }; my $c = $f->(); say $c;
### keys-count
my %h = (a=>1,b=>2); my $f = sub { return keys %h }; my $c = $f->(); say $c;
### last-stmt-hash
my %h = (a=>1,b=>2); my $f = sub { %h }; my $c = $f->(); say $c;
### last-stmt-map
my $f = sub { map { $_ } 1, 2, 3 }; my $c = $f->(); say $c;
### last-stmt-grep
my $f = sub { grep { $_ } 1, 2, 3 }; my $c = $f->(); say $c;
### last-stmt-sort
my $f = sub { sort 3, 2, 1 }; my $c = $f->(); say defined $c ? "def:$c" : "undef";
### last-stmt-assign-list
my $f = sub { my @x = (1, 2, 3) }; my $c = $f->(); say $c;
### last-stmt-listassign
my $f = sub { my ($p, $q) = (7, 8, 9) }; my $c = $f->(); say $c;
### last-stmt-slice
my @a = (1, 2, 3); my $f = sub { @a[0, 1] }; my $c = $f->(); say $c;
### last-stmt-call
sub two() { return (8, 9) } my $f = sub { two() }; my $c = $f->(); say $c;
