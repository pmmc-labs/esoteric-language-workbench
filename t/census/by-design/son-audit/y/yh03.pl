use v5.42;
sub c { wantarray ? "L" : "S" } sub g { return c() } my @l = g(); my $s = g(); print "@l$s\n";
