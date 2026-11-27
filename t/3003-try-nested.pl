# Tries in tries, in subs that call each other: a die goes to the nearest try
# open, through the frames between; a die in a catch to the one further out.
use v5.42;
no warnings 'recursion';
sub level($n) {
    return "bottom" if $n == 0;
    try {
        my $r = level($n - 1);
        die "odd $n\n" if $n % 2;
        return "$r<$n";
    } catch ($e) {
        die "rethrown at $n: $e" if $n % 3 == 0;
        return "caught at $n: $e";
    }
}
for my $n (1 .. 7) {
    try { print level($n), "\n" } catch ($e) { print "top: $e" }
}
my $deep = 0;
sub sink($n) { $deep = $n; die "sunk\n" if $n >= 400; return sink($n + 1) }
for my $round (1 .. 3) {
    try { sink(0) } catch ($e) { print "$round $deep $e" }
}
