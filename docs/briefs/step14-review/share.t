### while-my
my @q = (1, 2, 3); my @s;
while (my $x = shift @q) { push @s, sub { $x } }
say join ",", map { $_->() } @s;
### while-my-counter
my @q = (1, 2); my @s;
while (my $x = shift @q) { push @s, sub { $x++ } }
say $s[0]->(), $s[0]->(), $s[1]->();
### if-my
my @s; for my $i (1..2) { if (my $x = $i * 10) { push @s, sub { $x } } }
say join ",", map { $_->() } @s;
### if-my-elsif
my @s; for my $i (0..1) { if (my $x = $i) { push @s, sub { "a$x" } } elsif (my $y = 5) { push @s, sub { "b$x$y" } } }
say join ",", map { $_->() } @s;
### cfor-shared
my @s; for (my $i = 0; $i < 3; $i++) { push @s, sub { $i } }
say join ",", map { $_->() } @s;
### cfor-body-my
my @s; for (my $i = 0; $i < 3; $i++) { my $j = $i; push @s, sub { $j } }
say join ",", map { $_->() } @s;
### body-my-next
my @s; for my $i (1..3) { my $j = $i; push @s, sub { $j }; next if $i == 2; $j = $j * 10 }
say join ",", map { $_->() } @s;
### body-my-last
my @s; for my $i (1..3) { my $j = $i; push @s, sub { $j }; last if $i == 2; }
say join ",", map { $_->() } @s;
### my-before-closure-not-in-scope
my $f = sub { 1 }; my $y = 5; say $f->();
### self-in-init
my $f = sub { $f };
say "compiled";
### recursion-named-my
my @s;
sub rec($n) { my $v = $n; push @s, sub { $v }; rec($n - 1) if $n > 0; $v = $v * 10; return }
rec(2); say join ",", map { $_->() } @s;
### param-capture
sub mk($x) { return sub { $x++ } }
my $c = mk(5); say $c->(), $c->(), mk(5)->();
### param-default-closure
sub g($x, $f = sub { $x }) { $x = 9; return $f->() }
say g(1);
### param-default-closure-later-param
sub g2($x, $f = sub { $x }, $y = $f->()) { return $y }
say g2(3);
### array-capture-reached-again
my @s; for my $i (1..2) { my @a = ($i); push @s, sub { push @a, 0; scalar(@a) } }
say $s[0]->(), $s[0]->(), $s[1]->();
### array-capture-assign-empty
my @a = (1, 2); my $f = sub { scalar(@a) }; @a = (); say $f->();
### hash-capture
my %h; my $f = sub { $h{x}++ }; $f->(); $f->(); say $h{x};
### file-var-before-my-anon
my $f;
sub setup() { $f = sub { $later } }
setup(); my $later = 7; say $f->();
### map-block-my
my @s = map { my $v = $_; sub { $v } } 1 .. 3; say join ",", map { $_->() } @s;
### map-block-my-counter
my @s = map { my $v = $_; sub { $v++ } } 1 .. 2; say $s[0]->(), $s[0]->(), $s[1]->();
### grep-block-my
my @s; my @g = grep { my $v = $_; push @s, sub { $v }; 1 } 1 .. 3; say join ",", map { $_->() } @s;
### sort-block-my
my @s; my @o = sort { my $v = $a . $b; push @s, sub { $v }; $a <=> $b } 2, 1; say join ",", map { $_->() } @s;
### stmt-modifier-for-closure-my-outside
my @s; my $k = 0; push @s, sub { $k } for 1 .. 2; $k = 5; say join ",", map { $_->() } @s;
### if-block-my-in-loop
my @s; for my $i (1..2) { if ($i) { my $v = $i; push @s, sub { $v } } } say join ",", map { $_->() } @s;
### bare-block-in-loop
my @s; for my $i (1..2) { { my $v = $i; push @s, sub { $v } } } say join ",", map { $_->() } @s;
### until-loop-body-my
my @s; my $i = 0; until ($i == 2) { $i++; my $v = $i; push @s, sub { $v } } say join ",", map { $_->() } @s;
### while-modifier-shared
my @s; my $i = 0; push @s, sub { $i } while ++$i < 3; say join ",", map { $_->() } @s;
