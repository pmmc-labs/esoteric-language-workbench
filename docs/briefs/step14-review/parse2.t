### named-call-index
sub mk() { return [1, 2] } say mk()[1];
### named-call-arrow-index
sub mk() { return [1, 2] } say mk()->[1];
### named-call-call-arrow
sub mk() { return sub { 3 } } say mk()->()();
### paren-sub-call
say((sub { 4 })->());
### paren-sub-call-noarrow
say((sub { 4 })());
### call-call-call
my $f = sub { sub { sub { 5 } } }; say $f->()()();
### elem-call-call
my @a = (sub { sub { 6 } }); say $a[0]()();
### ref-call-index-call
my $r = [sub { [sub { 7 }] }]; say $r->[0]()[0]();
### deref-block-call
my $f = sub { 8 }; say &{ $f };
### call-ampersand-name
sub nm() { 9 } say &nm;
### call-ampersand-name-paren
sub nm() { 9 } say &nm();
### chain-arrow-call-after-key
my %h = (k => [sub { 10 }]); say $h{k}[0]();
### ref-ref-name-call-bareword
sub nm($x) { $x } my $r = \&nm; say $r->(1), &$r(2), &{$r}(3);
### stringify-code
my $f = sub { 1 }; say "f=$f" =~ /^f=CODE\(0x[0-9a-f]+\)$/ ? "addr" : "other";
### code-numeric
my $f = sub { 1 }; say $f + 0 > 0 ? "num" : "zero";
### code-eq-string
my $f = sub { 1 }; my $g = $f; say $f eq $g ? "eq" : "ne";
### ref-of-call-result-arrow
my $r = [sub { 1 }]; say ref $r->[0];
### ref-unary-sub
say ref sub { 1 };
### ref-unary-sub-call
say ref sub { [1] }->();
### defined-sub
my $f = sub { 1 }; say defined $f ? "d" : "u";
### defined-ampersand
sub nm() { 1 } say defined &nm ? "d" : "u";
### var-paren-not-say
my $f = sub { 1 }; my $v = $f(1); say $v;
### ref-name-arrow-call
sub nm() { sub { 5 } } my $r = \&nm->(); say ref($r);
### ref-name-brackets-arrow-call
sub nm() { 6 } say ((\&nm)->());
### ref-name-then-index
sub nm() { [7] } my $r = \&nm; say ref $r;
### ampersand-name-statement-passes-args
sub nm(@x) { scalar(@x) } sub wrap(@y) { &nm } say wrap(1, 2, 3);
### ref-name-arrow-call-clean
sub nm() { return sub { 42 } }
my $r = \&nm->();
say ref($r);
say $r->$*;
### ref-name-arrow-index
sub nm() { return [8, 9] }
my $r = \&nm->[1];
say ref($r), " ", $r->$*;
### ref-name-arrow-call-in-sub-with-args
sub nm() { return sub { 42 } }
sub outer($x) { my $r = \&nm->(); return ref($r) }
say outer(1);
