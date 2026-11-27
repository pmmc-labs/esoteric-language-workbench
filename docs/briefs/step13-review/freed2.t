### for-sort-replace
my $r = [3, 1, 2];
for my $x (sort { $a <=> $b } $r->@*) { $r = [7, 8, 9]; say $x; }
### for-grep-replace
my $r = [1, 2, 3];
for my $x (grep { 1 } $r->@*) { $r = [7, 8, 9]; say $x; }
### for-reverse-replace
my $r = [1, 2, 3];
for my $x (reverse $r->@*) { $r = [7, 8, 9]; say $x; }
### for-slice-replace
my $r = [1, 2, 3];
for my $x ($r->@[0, 1]) { $r = [7, 8, 9]; say $x; }
### for-elem-chain-single-replace
my $r = [[1, 2]];
for my $x ($r->[0]->@*) { $r->[0] = [8, 9]; say $x; }
### for-elems-replace
my $r = [1, 2];
for my $x ($r->[0], $r->[1]) { $r = [7, 8]; say $x; }
### for-hash-values-named-single
my %h = (a => 1, b => 1);
my $r = \%h;
for my $v (values $r->%*) { $r = {}; say $v; }
### for-map-replace
my $r = [1, 2, 3];
for my $x (map { $_ } $r->@*) { $r = [7, 8, 9]; say $x; }
### for-call-returning-elems
my $r = [1, 2, 3];
sub all() { return $r->@*; }
for my $x (all()) { $r = [7, 8, 9]; say $x; }
### for-scalar-deref-replace
my $x = 1; my $y = 2; my $r = \$x;
for my $v ($r->$*, 0) { $r = \$y; say $v; }
### for-scalar-deref-freed
sub mk() { my $t = 5; return \$t; }
my $r = mk();
for my $v ($r->$*, 0) { $r = mk(); say $v; }
### for-hash-elem-deref-delete
my %h = (a => [1, 2]);
for my $x ($h{a}[0], $h{a}[1]) { delete $h{a}; say $x; }
### for-named-array-elems-of-refs
my @a = ([1, 2]);
for my $x ($a[0][0], $a[0][1]) { $a[0] = [8, 9]; say $x; }
