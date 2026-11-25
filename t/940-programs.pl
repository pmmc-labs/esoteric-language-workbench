# Small programs the language can say now, each with a sub or more.
use v5.42;

sub fact($n) {
    return 1 if $n < 2;
    return $n * fact($n - 1);
}
say fact(0);
say fact(5);
say fact(20);

sub fib($n) {
    return $n < 2 ? $n : fib($n - 1) + fib($n - 2);
}
my $i = 0;
my $row = "";
while ($i < 15) {
    $row .= fib($i);
    $row .= " ";
    $i++;
}
say $row;

sub gcd($p, $q) {
    return $p unless $q;
    return gcd($q, $p % $q);
}
say gcd(1071, 462);
say gcd(17, 5);

sub ack($m, $n) {
    return $n + 1 if $m == 0;
    return ack($m - 1, 1) if $n == 0;
    return ack($m - 1, ack($m, $n - 1));
}
say ack(2, 3);

sub reversed($s) {
    return $s if length($s) < 2;
    return reversed(substr($s, 1)) . substr($s, 0, 1);
}
say reversed("a sub calls itself");

# The moves of the Tower of Hanoi, counted and not printed.
my $moves = 0;
sub hanoi($n, $from, $to, $via) {
    return if $n == 0;
    hanoi($n - 1, $from, $via, $to);
    $moves++;
    hanoi($n - 1, $via, $to, $from);
}
hanoi(10, "a", "c", "b");
say $moves;

sub is_prime($n) {
    return false if $n < 2;
    for (my $d = 2; $d * $d <= $n; $d++) {
        return false if $n % $d == 0;
    }
    return true;
}
my $primes = "";
for (my $k = 0; $k < 50; $k++) {
    $primes .= $k if is_prime($k);
    $primes .= " " if is_prime($k);
}
say $primes;

sub power($base, $exp, $acc = 1) {
    return $acc if $exp == 0;
    return power($base, $exp - 1, $acc * $base);
}
say power(2, 10);
say power(3, 4, 2);

sub collatz($n, $steps = 0) {
    return $steps if $n == 1;
    return collatz($n % 2 ? $n * 3 + 1 : $n / 2, $steps + 1);
}
say collatz(7);

sub pad($s, $width, $with //= " ") {
    $s = $with . $s while length($s) < $width;
    return $s;
}
say "[" . pad("7", 3) . "]";
say "[" . pad("42", 5, "0") . "]";
say "[" . pad("long", 2, undef) . "]";
