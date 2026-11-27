### slice-left-elems-right
my @a = (1, 2); my $r = \@a;
@a[0, 1] = ($r->[1], $r->[0]);
say "@a";
### elems-swap-via-ref
my @a = (1, 2); my $r = \@a;
($a[0], $a[1]) = ($r->[1], $r->[0]);
say "@a";
### scalar-swap-via-ref
my ($x, $y) = (1, 2); my $r = \$x;
($x, $y) = ($y, $r->$*);
say "$x $y";
### scalar-swap-via-ref2
my ($x, $y) = (1, 2); my $r = \$x;
($r->$*, $y) = ($y, $x);
say "$x $y";
### scalar-swap-via-ref3
my ($x, $y) = (1, 2); my $r = \$x; my $s = \$y;
($r->$*, $s->$*) = ($s->$*, $r->$*);
say "$x $y";
### ref-elems-swap
my $r = [1, 2]; my $s = $r;
($r->[0], $r->[1]) = ($s->[1], $s->[0]);
say "$r->[0] $r->[1]";
### ref-slice-swap
my $r = [1, 2]; my $s = $r;
$r->@[0, 1] = ($s->[1], $s->[0]);
say "$r->[0] $r->[1]";
### hash-slice-swap
my %h = (a => 1, b => 2); my $r = \%h;
@h{"a", "b"} = ($r->{b}, $r->{a});
say "$h{a} $h{b}";
### hash-elems-swap
my %h = (a => 1, b => 2); my $r = \%h;
($h{a}, $h{b}) = ($r->{b}, $r->{a});
say "$h{a} $h{b}";
### whole-from-elems
my @a = (1, 2); my $r = \@a;
@a = ($r->[1], $r->[0]);
say "@a";
### whole-ref-from-elems
my $r = [1, 2]; my $s = $r;
$r->@* = ($s->[1], $s->[0]);
say "$r->[0] $r->[1]";
### my-list-from
my @a = (1, 2); my $r = \@a;
my ($p, $q) = ($r->[1], $r->[0]);
say "$p $q";
### array-target-and-elem
my $r = [1, 2]; my $s = $r;
($s->[0], $r->@*) = (9, $s->[0], $s->[1]);
say join(",", $r->@*);
### nested-swap
my $r = [[1], [2]];
($r->[0][0], $r->[1][0]) = ($r->[1][0], $r->[0][0]);
say "$r->[0][0] $r->[1][0]";
### nested-swap-other
my $r = [[1], [2]]; my $t = $r->[0]; my $u = $r->[1];
($t->[0], $u->[0]) = ($r->[1][0], $r->[0][0]);
say "$r->[0][0] $r->[1][0]";
### deref-scalar-swap-cell
my ($x, $y) = (1, 2); my @refs = (\$x, \$y);
($x, $y) = ($refs[1]->$*, $refs[0]->$*);
say "$x $y";
