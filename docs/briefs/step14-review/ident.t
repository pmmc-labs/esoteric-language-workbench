### own-my-only
my @s; for my $i (1..2) { push @s, sub { my $y = 1; $y } }
say $s[0] == $s[1] ? "same" : "diff";
### file-var
my $g = 1; my @s; for my $i (1..2) { push @s, sub { $g } }
say $s[0] == $s[1] ? "same" : "diff";
### file-array
my @g = (1); my @s; for my $i (1..2) { push @s, sub { $g[0] } }
say $s[0] == $s[1] ? "same" : "diff";
### file-hash
my %g = (a => 1); my @s; for my $i (1..2) { push @s, sub { $g{a} } }
say $s[0] == $s[1] ? "same" : "diff";
### outer-only-in-nested
my $g = 1; my @s; for my $i (1..2) { push @s, sub { sub { $g } } }
say $s[0] == $s[1] ? "same" : "diff";
### outer-only-in-nested-loopvar
my @s; for my $i (1..2) { push @s, sub { sub { $i } } }
say $s[0] == $s[1] ? "same" : "diff";
### current-sub
my @s; for my $i (1..2) { push @s, sub { __SUB__ } }
say $s[0] == $s[1] ? "same" : "diff";
### current-sub-self
my $f = sub { __SUB__ }; say $f->() == $f ? "same" : "diff";
### named-sub-call
sub nm() { 1 } my @s; for my $i (1..2) { push @s, sub { nm() } }
say $s[0] == $s[1] ? "same" : "diff";
### named-sub-ref
sub nm2() { 1 } my @s; for my $i (1..2) { push @s, sub { \&nm2 } }
say $s[0] == $s[1] ? "same" : "diff";
### in-named-sub-no-outer
sub mk() { return sub { 1 } } say mk() == mk() ? "same" : "diff";
### in-named-sub-param
sub mk2($x) { return sub { 1 } } say mk2(1) == mk2(2) ? "same" : "diff";
### in-named-sub-capture-file
my $g = 0; sub mk3() { return sub { $g } } say mk3() == mk3() ? "same" : "diff";
### recursion-same-expr
my @s; sub rec($n) { push @s, sub { 1 }; rec($n - 1) if $n > 0; return }
rec(2); say $s[0] == $s[1] ? "same" : "diff", " ", $s[1] == $s[2] ? "same" : "diff";
### recursion-closure
my @s; sub rec2($n) { push @s, sub { $n }; rec2($n - 1) if $n > 0; return }
rec2(2); say join ",", map { $_->() } @s; say $s[0] == $s[1] ? "same" : "diff";
### dollar-underscore-in-sub
my @s; for my $i (1..2) { push @s, sub { $_ } }
say $s[0] == $s[1] ? "same" : "diff";
### non-closure-outer-shadow-param
my $x = 1; my @s; for my $i (1..2) { push @s, sub ($x) { $x } }
say $s[0] == $s[1] ? "same" : "diff";
### constant-expr
my @s; for my $i (1..2) { push @s, sub { 1 + 2 } }
say $s[0] == $s[1] ? "same" : "diff";
### non-closure-holds-state-via-my? 
my @s; for my $i (1..2) { push @s, sub { my @l; push @l, 1; scalar(@l) } }
say $s[0]->(), $s[0]->(), $s[1]->();
### closure-in-closure-no-outer
my $f = sub { sub { 1 } }; say $f->() == $f->() ? "same" : "diff";
### closure-made-by-two-calls-of-closure-outer
my $f = sub ($y) { sub { $y } }; say $f->(1) == $f->(1) ? "same" : "diff";
### file-var-declared-later-named
sub uses() { return sub { 1 } }
my $later = 1;
say uses() == uses() ? "same" : "diff";
### ref-of-captured-var-identity
my $x = 1; my $f = sub { \$x }; say $f->() == \$x ? "same" : "diff";
### inner-plain-in-two-outer-clones
my $g = 1; my @o; for my $i (1..2) { push @o, sub { $g; sub { 1 } } }
say $o[0] == $o[1] ? "outer same" : "outer diff"; say $o[0]->() == $o[1]->() ? "inner same" : "inner diff";
### inner-plain-in-outer-clone-param
my $mk = sub ($y) { sub { 1 } }; say $mk->(1) == $mk->(2) ? "same" : "diff";
### inner-plain-in-named-sub-clones
my $g = 1; sub outer() { return sub { $g; return sub { 2 } } } say outer()->() == outer()->() ? "same" : "diff";
### inner-plain-in-two-outer-clones-loopvar
my @o; for my $i (1..2) { push @o, sub { $i; sub { 1 } } }
say $o[0]->() == $o[1]->() ? "inner same" : "inner diff";
### inner-uses-only-current-sub
my @o; for my $i (1..2) { push @o, sub { $i; sub { __SUB__ } } }
say $o[0]->() == $o[1]->() ? "inner same" : "inner diff";
