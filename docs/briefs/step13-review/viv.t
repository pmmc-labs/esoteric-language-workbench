### viv-list-scalar
my $r;
my @l = ($r, ($r->[0] = 1));
say defined $l[0] ? "defined " . ref($l[0]) : "undef";
### viv-list-sub
my $cfg;
sub get() { $cfg->{x} = 1; return 0; }
my @l = ($cfg, get());
say defined $l[0] ? "defined " . ref($l[0]) : "undef";
### viv-for-block
my $r;
for my $v ($r, $r) {
    say defined $v ? "d " . ref($v) : "u";
    push $r->@*, 1;
}
### viv-for-block-sub
my $r;
sub grow() { $r->{k}++; }
for my $v ($r, 1) {
    grow();
    say ref($v) eq "" ? "plain" : ref($v);
}
### viv-elem-list
my @a = (undef);
my @l = ($a[0], ($a[0][0] = 1));
say ref($l[0]) eq "" ? "plain" : ref($l[0]);
### viv-helem-list
my %h = (a => undef);
my @l = ($h{a}, ($h{a}{b} = 1));
say ref($l[0]) eq "" ? "plain" : ref($l[0]);
### viv-helem-missing-list
my %h;
my @l = ($h{a}, ($h{a}{b} = 1));
say ref($l[0]) eq "" ? "plain" : ref($l[0]);
### viv-values-loop
my %h = (a => undef);
for my $v (values %h) { $h{a}{x} = 1; say ref($v) eq "" ? "plain" : ref($v); }
### viv-array-loop
my @a = (undef, undef);
for my $v (@a) { $a[1][0] = 1; say ref($v) eq "" ? "plain" : ref($v); }
### viv-and-operand
my $r;
my @l = ($r && 1, ($r->[0] = 1));
say ref($l[0]) eq "" ? "plain" : ref($l[0]);
### viv-arg
my $r;
sub f($p, $q) { say ref($p) eq "" ? "plain" : ref($p); }
f($r, ($r->[0] = 1));
### viv-ternary-store
my ($r, $s);
my $c = 1;
($c ? $r : $s)->[0] = 5;
say ref($r) eq "" ? "plain" : ref($r), " ", defined $s ? "s" : "nos";
### viv-or-store
my ($r, $s);
($r || $s)->[0] = 5;
say ref($r) eq "" ? "rplain" : ref($r), " ", ref($s) eq "" ? "splain" : ref($s);
### viv-dor-store
my ($r, $s);
($r // $s)->[0] = 5;
say ref($r) eq "" ? "rplain" : ref($r), " ", ref($s) eq "" ? "splain" : ref($s);
### viv-assign-store
my $x;
($x = undef)->[0] = 5;
say ref($x) eq "" ? "plain" : ref($x);
### viv-call-store
sub f() { return undef; }
f()->[0] = 5;
say "after";
### viv-call-store2
sub f() { return; }
f()->[0] = 5;
say "after";
### viv-call-store3
my $r;
sub f() { return $r; }
f()->[0] = 5;
say "after ", defined $r ? "r" : "nor";
### viv-call-store4
sub f() { my $x; return $x; }
f()->{a}{b} = 5;
say "after";
### viv-undef-store
(undef)->[0] = 5;
say "after";
### viv-call-plusplus
sub f() { return undef; }
f()->[0]++;
say "after";
### viv-call-push
sub f() { return undef; }
push f()->@*, 1;
say "after";
