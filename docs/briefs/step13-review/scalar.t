### while-my-ref
my @a = (1, 2, 3); my @r;
while (my $x = shift @a) { push @r, \$x; }
say join ",", map { defined $_->$* ? $_->$* : "u" } @r;
### while-my-ref-last
my $n = 0; my @r;
while (my $x = ++$n) { push @r, \$x; last if $n == 3; }
say join ",", map { $_->$* } @r;
### until-my-ref
my $n = 0; my @r;
until ((my $x = ++$n) > 3) { push @r, \$x; }
say join ",", map { $_->$* } @r;
### for-c-my-ref
my @r;
for (my $i = 0; $i < 3; $i++) { push @r, \$i; }
say join ",", map { $_->$* } @r;
### if-my-ref-loop
my @r;
for my $k (1 .. 3) { if ((my $x = $k) > 0) { push @r, \$x; } }
say join ",", map { $_->$* } @r;
### block-my-ref-loop
my @r;
for my $k (1 .. 3) { my $x = $k; push @r, \$x; }
say join ",", map { $_->$* } @r;
### block-my-noinit-ref-loop
my @r;
for my $k (1 .. 3) { my $x; $x = $k if $k == 1; push @r, \$x; }
say join ",", map { defined $_->$* ? $_->$* : "u" } @r;
### while-my-noinit
my $n = 0; my @r;
while ($n < 3) { $n++; my $x; $x = $n if $n == 1; push @r, \$x; }
say join ",", map { defined $_->$* ? $_->$* : "u" } @r;
### file-var-before-my
sub f() { return \$x; }
my $x = 5;
say f()->$*;
### ref-ref
my $x = 5; my $r = \$x; my $s = \$r;
say ref $s, " ", ref $r, " ", $s->$*->$*;
### ref-of-ref-later
my $x = 5; my $r = \$x; say ref $r; $x = [1]; say ref $r;
### scalar-ref-eq
my $x = 1; say \$x == \$x ? "same" : "diff";
### param-ref
sub f($p) { my $r = \$p; $r->$* = 9; return $p; }
my $v = 1; say f($v), " ", $v;
### deref-assign-ops
my $x = 1; my $r = \$x;
$r->$* .= "a"; ${ $r } .= "b"; $r->$*++; say $x;
### deref-plusplus-str
my $x = "a9"; my $r = \$x; $r->$*++; say $x;
### store-undef-scalar
my $s; $s->$* = 5; say ref $s, " ", $s->$*;
### store-undef-scalar-braces
my $s; ${ $s } = 5; say ref $s;
### ref-bool-x
my $r = [1]; say "a" x !!$r;
### ref-in-ternary-numeric
my $r = [1]; my $s = $r; say(($r == $s) + 0);
