# Lists returned, slurpy parameters, join and reverse, by hand, with perl's
# answers: what the model of step 10a does not write.
use v5.42;

# Without brackets, and one inside another.
my @a = (3, 1, 2);
say join ",", reverse 1 .. 3;
say join "-", @a, "z";
print join(", ", @a), "\n";
my @b = reverse @a, 9;
say @b;
push @b, reverse @a;
say @b;
my $s = join "", reverse(@a);
say $s;
say "n: " . join(",", @a) . "!";
say length join("", @a);
say uc join "-", "a", "b";
say join(",", @a,);
say reverse "a", "b";

# A list built up by a sub that calls itself, and taken apart by another.
sub digits($n) {
    return ($n) if $n < 10;
    return (digits(($n - $n % 10) / 10), $n % 10);
}
sub total(@v) {
    my $t = 0;
    for my $x (@v) {
        $t += $x;
    }
    return $t;
}
say join("+", digits(40961)), "=", total(digits(40961));

# The first and the rest, the usual way.
sub largest($first, @rest) {
    my $most = $first;
    for my $x (@rest) {
        $most = $x if $x > $most;
    }
    $most
}
say largest(3, 9, 4), largest(7), largest(@a, 2);

# A sub that gives a pair, taken by a list assignment; and swapped.
sub divide($n, $d) {
    return (($n - $n % $d) / $d, $n % $d);
}
my ($q, $r) = divide(17, 5);
say $q, " r ", $r;
($r, $q) = divide(9, 2);
say $q, $r;

# Its last statement, a list: an array, and a list of calls.
sub twice(@v) { (@v, @v) }
sub wrap($x) { ("<", $x, ">") }
say twice(1, 2), "|", wrap(join("", twice("ab")));
my @w = (wrap(1), wrap(2))[1, 4];
say @w;

# A list of none, of one, and through a sub that hands it on.
sub none() { return (); }
sub one() { return (7,); }
sub pass($c) { return $c ? one() : none(); }
my @n = (none(), pass(0), pass(1), one());
say scalar(@n), @n;
my $o = pass(1);
say $o, defined(pass(0)) ? "def" : "undef";

# A sub's array is its own: what it returns is a copy.
sub fresh() {
    my @mine = (1, 2);
    push @mine, 3;
    return @mine;
}
my @f = fresh();
push @f, fresh();
say scalar(@f), join("", @f);

# A loop over what a sub returned freezes nothing.
for my $x (fresh()) {
    push @a, $x;
}
say join(",", @a);

# A slurpy with nothing left, and with the same name as a scalar.
sub both($x, @x) { return $x . scalar(@x) . join("", @x); }
say both(1), both(1, 2, 3);
sub count(@) { return "any"; }
sub head($x, @) { return $x; }
say count(), count(1, 2), head(7, 8);

# A sub is known to give a list by a `return` anywhere in it, by its last
# statement, and by handing on a call of one that does: each as the one
# argument of another call.
sub relay() { return digits(12); }
sub first_over($least, @v) {
    for my $x (@v) {
        return ($x, $x) if $x > $least;
    }
    return ();
}
sub maybe($c) {
    if ($c) {
        return (1, 2);
    }
    return ();
}
say total(relay()), total(twice(1, 2)), total(first_over(1, 1, 2, 3)), total(maybe(1)), total(maybe(0));
