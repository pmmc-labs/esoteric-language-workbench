### loopvar-viv
my @l = (undef, undef);
for my $x (@l) { $x->[0] = 1; }
say join ",", map { ref($_) || "plain" } @l;
### loopvar-viv-push
my @l = (undef);
for my $x (@l) { push $x->@*, 1; }
say join ",", map { ref($_) || "plain" } @l;
### dollar-underscore-viv
my @l = (undef, undef);
$_->{n} = 1 for @l;
say join ",", map { ref($_) || "plain" } @l;
### map-viv
my @l = (undef);
my @m = map { $_->[0] = 1; 0 } @l;
say join ",", map { ref($_) || "plain" } @l;
### grep-viv
my %h = (a => undef);
my @m = grep { $_->[0] = 1; 0 } values %h;
say ref($h{a}) || "plain";
### loopvar-viv-hashvalues
my %h = (a => undef);
for my $v (values %h) { $v->{z} = 1; }
say ref($h{a}) || "plain";
### loopvar-viv-literal
for my $x (undef) { $x->[0] = 1; }
say "after";
### loopvar-viv-scalarvar
my $s;
for my $x ($s) { $x->[0] = 1; }
say ref($s) || "plain";
### loopvar-viv-call
sub f() { return undef; }
for my $x (f()) { $x->[0] = 1; }
say "after";
### loopvar-store-through-defined
my @l = ([0]);
for my $x (@l) { $x->[0] = 1; }
say $l[0][0];
### sort-a-viv
my @l = (undef, undef);
my @s = sort { $a->[0] = 1; 0 } @l;
say join ",", map { ref($_) || "plain" } @l;
### param-viv
sub f($p) { $p->[0] = 1; return 0; }
my $s; f($s); say ref($s) || "plain";
