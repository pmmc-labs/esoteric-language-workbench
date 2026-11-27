### say-sub-call
say sub { 3 }->();
### print-sub
print sub { 1 }; print "\n";
### stmt-start-sub-call
sub { say "ran" }->();
### stmt-start-sub-call-semicolon
sub { say "ran" }->(); say "after";
### sub-then-bracket
my $f = sub { [1, 2] }->()[1]; say $f;
### call-then-index-noarrow
my $f = sub { [5, 6] }; say $f->()[1];
### call-then-key-noarrow
my $f = sub { { k => 7 } }; say $f->(){k};
### call-then-key-plus
my $f = sub { +{ k => 7 } }; say $f->(){k};
### sub-returning-hash-word-first
my $f = sub { { a => 1 } }; say ref($f->()) || "plain:" . join(",", $f->());
### sub-returning-hash-scalar-first
my $x = "a"; my $f = sub { { $x => 1 } }; my @r = $f->(); say scalar(@r), ref($r[0]) || "plain";
### elem-call-noarrow
my @r = (sub { 8 }); say $r[0]();
### ref-elem-call-noarrow
my $r = [sub { 9 }]; say $r->[0]();
### hash-call-noarrow
my %h = (k => sub ($x) { $x * 2 }); say $h{k}(4);
### var-bracket
my $f = sub { 1 }; say $f(1);
### var-space-bracket
my $f = sub { 1 }; say $f (1);
### arrow-space
my $f = sub ($x) { $x }; say $f-> (5);
### arrow-newline
my $f = sub ($x) { $x }; say $f
  ->(6);
### arrow-paren-newline
my $f = sub ($x) { $x }; say $f->
(7);
### ampersand-call
my $f = sub { 2 }; say &$f();
### ampersand-brace
my $f = sub { 2 }; say &{$f}();
### ampersand-postfix
my $f = sub { 2 }; say $f->&*;
### ref-name-call
sub nm($x) { $x + 1 } my $r = \&nm(1); say ref($r), " ", $r->$*;
### ref-name-call-space
sub nm2($x) { $x + 1 } my $r = \&nm2 (1); say ref($r);
### ref-name-noargs
sub nm3() { 5 } my $r = \&nm3; say $r->();
### ref-undefined-name
my $r = \&nosuch; say ref($r); say defined &nosuch ? "d" : "u";
### ref-name-before-defined
my $r = \&later; sub later() { 4 } say $r->();
### ref-deref-var
my $f = sub { 3 }; my $r = \&$f; say $r == $f ? "same" : "diff";
### ref-string
sub nm4() { 1 } my $r = \&{"nm4"}; say $r->();
### current-sub-outside
say defined __SUB__ ? "def" : "undef";
### current-sub-named
sub nm5() { return __SUB__ } say nm5() == \&nm5 ? "same" : "diff";
### current-sub-in-map
my $f = sub { my @l = map { __SUB__ } 1; return $l[0] }; say $f->() == $f ? "same" : "diff";
### current-sub-in-sort
my $f = sub { my $s; my @l = sort { $s = __SUB__; $a <=> $b } 2, 1; return $s }; say $f->() == $f ? "same" : "diff";
### current-sub-in-grep
my $f = sub { my @l = grep { __SUB__ } 1; return scalar(@l) }; say $f->();
### proto-dollar
my $f = sub ($) { 1 }; say $f->(9);
### proto-dollar-dollar
my $f = sub ($$) { 1 }; say $f->(9, 8);
### sig-placeholder-default
my $f = sub ($x, $y = 1, @) { $x + $y }; say $f->(1, 2, 3, 4);
### sig-at-underscore
my $f = sub (@_) { 1 }; say $f->();
### attr
my $f = sub :prototype($) { 1 }; say $f->(1);
### attr-lvalue
my $x = 1; my $f = sub :lvalue { $x }; $f->() = 5; say $x;
### named-sub-no-sig-stmt
sub name { 1 } say name();
### sub-paren-named
sub name2 ($x) { $x } say name2(3);
### anon-sig-param-shadows
my $x = 1; my $f = sub ($x) { $x + 1 }; say $f->(10);
### anon-my-shadows
my $x = 1; my $f = sub { my $x = $x + 1; $x }; say $f->(), $x;
### return-in-map-in-anon
my $f = sub { my @l = map { return 5 } 1, 2; 9 }; say $f->();
### last-in-map-in-anon-own-loop
my $f = sub { my $n = 0; for my $i (1..3) { my @l = map { last if $i == 2; $_ } 1; $n++ } return $n }; say $f->();
### next-in-anon-to-own-loop
my $f = sub { my $n = 0; for my $i (1..3) { next if $i == 2; $n++ } return $n }; say $f->();
### last-crossing-sub-in-sort
my @l; for my $i (1..3) { @l = sort { last } 2, 1; say $i } say "done";
### anon-hash-of-subs
my %d = (inc => sub ($n) { $n + 1 }, dec => sub ($n) { $n - 1 }); say $d{inc}->(1), $d{dec}->(1);
### sub-in-list-comma
my @l = (sub { 1 }, sub { 2 }); say scalar(@l);
### sub-then-x
my @l = (sub { 1 }) x 2; say $l[0] == $l[1] ? "same" : "diff";
### double-call
my $f = sub { sub { 3 } }; say $f->()->(), $f->()();
### block-stmt-sub-word
my $f = sub { sub { 1 } }; say ref($f->());
### say-paren-sub
say(sub { 4 }->());
### ternary-subs
my $f = 1 ? sub { "a" } : sub { "b" }; say $f->();
### or-sub
my $g; my $f = $g || sub { "dflt" }; say $f->();
### sub-call-wrongcount
my $f = sub ($x) { $x }; say $f->();
### arrow-call-on-call
sub mk() { return sub { 11 } } say mk()->();
### arrow-call-on-call-noarrow
sub mk2() { return sub { 12 } } say mk2()();
