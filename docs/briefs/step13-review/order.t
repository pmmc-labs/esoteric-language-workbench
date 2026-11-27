### store-self-viv
my $r; $r->[0] = $r;
say defined $r->[0] ? ref($r->[0]) . ($r->[0] == $r ? " self" : " other") : "undef";
### store-self-viv-hash
my %h = (a => undef); $h{a}{b} = $h{a};
say defined $h{a}{b} ? ref($h{a}{b}) : "undef";
### store-self-viv-missing
my %h; $h{a}{b} = $h{a};
say defined $h{a}{b} ? ref($h{a}{b}) : "undef";
### store-self-viv-dor
my $r; $r->[0] = $r // 7;
say defined $r->[0] ? (ref($r->[0]) || $r->[0]) : "undef";
### store-self-viv-and
my $r; $r->{a} = $r && 1;
say defined $r->{a} ? (ref($r->{a}) || $r->{a}) : "undef";
### store-self-viv-ternary
my $r; my $c = 1; $r->[0] = $c ? $r : 0;
say defined $r->[0] ? (ref($r->[0]) || $r->[0]) : "undef";
### store-self-viv-paren
my $r; $r->[0] = ($r);
say defined $r->[0] ? (ref($r->[0]) || $r->[0]) : "undef";
### store-other-viv
my $r; my $s; $r->[0] = $s; say defined $r->[0] ? "def" : "undef";
### aassign-self-viv
my $r; my $x; ($r->[0], $x) = ($r, 1);
say defined $r->[0] ? ref($r->[0]) : "undef";
### opassign-self-viv
my $r; $r->[0] //= $r;
say defined $r->[0] ? ref($r->[0]) : "undef";
### store-elem-viv-sub
my $r;
sub peek() { return defined $r ? "made" : "not yet"; }
$r->[0] = peek();
say $r->[0];
### store-index-call-viv
my $r;
sub idx() { say defined $r ? "made" : "not yet"; return 0; }
$r->[idx()] = 1;
### store-two-hop-call-viv
my $r;
sub idx() { say defined $r->[0] ? "made" : "not yet"; return 0; }
$r->[0][idx()] = 1;
### opassign-index-call-viv
my $r;
sub idx() { say defined $r ? "made" : "not yet"; return 0; }
$r->[idx()] += 1;
### opassign-rhs-call-viv
my $r;
sub v() { say defined $r ? "made" : "not yet"; return 1; }
$r->[0] += v();
### push-arg-viv
my $r;
sub v() { say defined $r ? "made" : "not yet"; return 1; }
push $r->@*, v();
### aassign-viv-order
my $r;
sub v() { say defined $r ? "made" : "not yet"; return 1; }
($r->[0], $r->[1]) = (v(), 2);
### slice-left-viv-order
my $r;
sub v() { say defined $r ? "made" : "not yet"; return 1; }
$r->@[0, 1] = (v(), 2);
### whole-left-viv-order
my $r;
sub v() { say defined $r ? "made" : "not yet"; return 1; }
$r->@* = (v(), 2);
### plusplus-index-call
my $r;
sub idx() { say defined $r ? "made" : "not yet"; return 0; }
$r->[idx()]++;
