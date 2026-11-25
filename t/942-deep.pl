# Deeper than perl warns of, which is 100 calls of one sub: nothing
# happens there, and the line below keeps perl as quiet (D67).
use v5.42;
no warnings 'recursion';

sub depth($n) {
    return $n == 0 ? 0 : 1 + depth($n - 1);
}
say depth(99);
say depth(100);
say depth(3000);

sub even($n) { return $n == 0 ? true : odd($n - 1); }
sub odd($n) { return $n == 0 ? false : even($n - 1); }
say even(3000) ? "even" : "odd";
say even(2999) ? "even" : "odd";

# By way of a default.
sub chain($n, $rest = $n == 0 ? 0 : chain($n - 1)) {
    return $rest + 1;
}
say chain(2000);

my $sum = 0;
sub add_down($n) {
    $sum += $n;
    add_down($n - 1) if $n > 0;
}
add_down(3000);
say $sum;
