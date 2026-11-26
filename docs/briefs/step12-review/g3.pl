use v5.42;
# G3: a slice on the left with too few values stores undef in the rest,
# and so makes them.
my %h; my @a; my @b;
@h{"a", "b"} = (1);
say exists $h{b} ? "made" : "not made";
@a[1, 2] = (5);  say scalar(@a);
@b[2, 1] = ();   say scalar(@b);
# and with too many, the rest is dropped; a key twice keeps the last
@h{"a", "a"} = (8, 9, 10); say $h{a};
# every index before any store (D80), for a slice among other targets
my $i = "p";
($i, @h{$i, "q"}) = ("z", 1, 2);
say join ",", sort keys %h;
