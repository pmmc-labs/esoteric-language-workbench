### if-assign-anon
if (my $f = sub { 1 }) { say "t" }
### if-anon
if (sub { 0 }) { say "t" }
### not-anon
say !sub { 0 } ? "t" : "f";
### and-anon
my $x = sub { 0 } && 5; say $x;
### anon-in-bool-ternary
say sub { 0 } ? "t" : "f";
### while-assign-anon
my $n = 0; while (my $f = sub { 1 }) { last if ++$n > 1 } say $n;
### unless-anon-assign
my $f; unless ($f = sub { 0 }) { say "u" } say "ok";
### anon-sub-outer-my-later-same-name
my $f = sub { 1 }; my $f2 = $f; say $f2->();
### closure-over-loopvar-in-modifier-for
my @s; push @s, sub { 1 } for 1 .. 2; say scalar(@s);
### anon-sub-uses-var-of-same-statement-my
my ($x, $f) = (5, sub { 1 }); say $f->();
### masked-sig
my $x = 1; my $f = sub ($x, $x2) { $x }; say $f->(3, 4);
### sig-dup-param
my $f = sub ($x, $x) { $x }; say $f->(1, 2);
### exiting-sub-next
my $f = sub { next }; for my $i (1..2) { $f->(); say $i } say "done";
### exiting-sub-labeled
my $f = sub { last OUT }; OUT: for my $i (1..2) { $f->(); say $i } say "done";
### last-in-anon-own-loop
my $f = sub { for my $i (1..3) { last if $i == 2; say $i } return "r" }; say $f->();
### return-at-top-in-anon-in-loop
my $f = sub { for my $i (1..3) { return $i if $i == 2 } return 0 }; say $f->();
### same-statement-list-my-capture
my ($x, $f) = (5, sub { $x }); say $f->();
### self-array-init
my @fs = (sub { scalar(@fs) }); say $fs[0]->();
### outer-same-name-init
my $f = sub { "outer" }; { my $f = sub { $f->() . "+inner" }; say $f->(); }
### default-captures-earlier-param
my $f = sub ($x, $g = sub { $x * 2 }) { $g->() }; say $f->(4);
### default-captures-later-param
my $f = sub ($x = sub { $y }, $y = 1) { 1 }; say $f->();
