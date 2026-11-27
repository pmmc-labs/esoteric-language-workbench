### callee-reassigned-in-args
my $f = sub ($x) { "old$x" }; my $g = sub ($x) { "new$x" };
say $f->(($f = $g) ? 1 : 0);
### callee-reassigned-by-sub-in-args
my $f = sub ($x) { "old$x" };
sub swap() { $f = sub ($x) { "new$x" }; return 1 }
say $f->(swap());
### callee-key-changed-in-args
my %d = (a => sub ($x) { "A$x" }, b => sub ($x) { "B$x" }); my $k = "a";
say $d{$k}->($k = "b");
### callee-elem-shift-in-args
my @a = (sub ($x) { "first$x" }, sub ($x) { "second$x" });
say $a[0]->(scalar(shift @a) ? 1 : 0);
### callee-noarrow-elem
my @a = (sub ($x) { "first$x" }, sub ($x) { "second$x" });
say $a[0](scalar(shift @a) ? 1 : 0);
### callee-chain-call
my $f = sub { sub ($x) { "inner-old$x" } }; my $g = sub { sub ($x) { "inner-new$x" } };
say $f->()->(($f = $g) ? 1 : 0);
### callee-closure-changes-itself
my $f; $f = sub ($x) { "one$x" };
my $set = sub { $f = sub ($x) { "two$x" }; 7 };
say $f->($set->());
### callee-ref-name
sub one($x) { "one$x" } sub two($x) { "two$x" }
my $r = \&one; say $r->(($r = \&two) ? 1 : 0);
### callee-in-concat
my $f = sub { "old" };
say "x" . $f->() . (($f = sub { "new" }) ? "" : "");
### callee-counts
my $n = 0; my $f = sub ($x) { "f$x" };
say $f->($n++), $n;
### callee-after-args-order-print
my $f = sub ($x) { say "called"; $x };
sub arg() { say "arg"; 1 }
sub fn() { say "fn"; $f }
fn()->(arg());
### callee-call-order-two-args
sub arg($n) { say "arg$n"; $n }
sub fn() { say "fn"; sub ($p, $q) { "done" } }
say fn()->(arg(1), arg(2));
### callee-elem-index-call-order
sub idx() { say "idx"; 0 }
sub arg() { say "arg"; 1 }
my @a = (sub ($x) { "called$x" });
say $a[idx()]->(arg());
### callee-changes-arg-value
my $x = 1;
sub mk() { $x = 5; return sub ($v) { $v } }
say mk()->($x + 0);
### callee-changes-arg-var
my $x = 1;
sub mk() { $x = 5; return sub ($v) { $v } }
say mk()->($x);
### callee-changes-arg-elem
my @a = (1);
sub mk() { $a[0] = 5; return sub ($v) { $v } }
say mk()->($a[0] * 1);
### callee-index-reads-var-changed-by-arg
my $i = 0; my @fs = (sub { "zero" }, sub { "one" });
say $fs[$i]->($i = 1);
### callee-concat-arg
my $x = "a";
sub mk() { $x = "b"; return sub ($v) { $v } }
say mk()->($x . "!");
### callee-string-arg
my $x = "a";
sub mk() { $x = "b"; return sub ($v) { $v } }
say mk()->("$x!");
### callee-count-faults-order
sub mk() { say "mk"; return sub ($v) { $v } }
sub two() { say "two"; return (1, 2) }
say mk()->(two());
### callee-undef-order
my $f;
sub arg() { say "arg ran"; 1 }
$f->(arg());
### callee-not-code-order
my $f = [1];
sub arg() { say "arg ran"; 1 }
$f->(arg());
### order-curried
sub p($s) { say $s; 1 }
my $f = sub ($a1) { say "f called"; sub ($b1) { say "inner called"; 0 } };
$f->(p("a1"))->(p("a2"));
### order-curried-noarrow
sub p($s) { say $s; 1 }
my $f = sub ($a1) { say "f called"; sub ($b1) { say "inner called"; 0 } };
$f->(p("a1"))(p("a2"));
### order-dispatch-key-call
sub p($s) { say $s; $s }
my %d = (k => sub ($x) { say "called $x"; 0 });
$d{p("k")}->(p("arg"));
### order-callee-in-list
sub p($s) { say $s; 1 }
my $f = sub ($x) { say "called"; 2 };
my @l = (p("before"), $f->(p("arg")), p("after"));
