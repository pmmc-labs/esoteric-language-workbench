### interp-chain-then-assign
my $r = [3]; say "$r->[0]-" . ($r->[0] = 5);
### interp-chain-two-then-assign
my $r = [3]; my $x = 1; say "$r->[0]$x" . ($r->[0] = 5);
### concat-chain-late
my $r = [3]; say $r->[0] . "-" . ($r->[0] = 5);
### concat-deref-scalar-late
my $x = 3; my $r = \$x; say $r->$* . "-" . ($x = 5);
### interp-deref-scalar
my $x = 3; my $r = \$x; say "${ $r }-" . ($x = 5);
### interp-postfix-scalar
my $x = 3; my $r = \$x; say "$r->$*-" . ($x = 5);
### interp-at-star
my $r = [3, 4]; say "$r->@*-" . ($r->[0] = 5);
### interp-at-braces
my $r = [3, 4]; say "@{ $r }-" . ($r->[0] = 5);
### interp-lastidx
my $r = [3, 4]; say "$r->$#*-" . (push($r->@*, 5));
### interp-nested
my $r = [[3]]; say "$r->[0][0]-" . ($r->[0][0] = 5);
### interp-helem-chain
my %h = (a => {b => 3}); say "$h{a}{b}-" . ($h{a}{b} = 5);
### interp-alone-arg
my $r = [3]; sub f($s, $t) { return "$s$t"; } say f("$r->[0]", ($r->[0] = 5));
### interp-in-list
my $r = [3]; my @l = ("$r->[0]", ($r->[0] = 5)); say "@l";
### interp-chain-elem-assign-t230
my $r = []; my $i = 0; $r->[$i = 2] = "$i v"; say $r->[2];
### interp-chain-elem-assign-t230-chain
my $r = []; my $s = [0]; $r->[$s->[0] = 2] = "$s->[0] v"; say $r->[2];
### interp-chain-key-assign
my %h; my $s = {k => "a"}; $h{$s->{k} = "b"} = "$s->{k}!"; say join ",", %h;
### concat-assign-dot-eq
my $r = ["a"]; my $t = "x"; $t .= $r->[0] . ($r->[0] = "b"); say $t;
