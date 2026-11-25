use v5.42;
# `last` and `next` under a `for` modifier leave the modifier's own loop.
for my $i (1 .. 3) { last for 1, 2; print $i; }
say "";
for my $i (1 .. 3) { next for 1, 2; print $i; }
say "";
sub first() { return $_ for 4, 5; return 9 }
say first();
# a slurpy parameter is filled when its turn comes: after the arguments have all run, and after a default
my $v = 1;
sub bump() { $v = 9; return 5 }
sub f($x, @rest) { return "$x|@rest" }
say f(1, $v, bump()); $v = 1;
sub g($x, $y //= bump(), @rest) { return "$x|$y|@rest" }
say g(1, undef, $v);
