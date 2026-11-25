# Small programs that the language can now say: counting, searching,
# building strings. perl prints the same for each.
use v5.42;
# FizzBuzz.
for (my $n = 1; $n <= 15; $n++) {
    if ($n % 15 == 0) {
        say "FizzBuzz";
    } elsif ($n % 5 == 0) {
        say "Buzz";
    } elsif ($n % 3 == 0) {
        say "Fizz";
    } else {
        say $n;
    }
}
# The greatest common divisor, by Euclid.
my $p = 1071;
my $q = 462;
while ($q != 0) {
    my $r = $p % $q;
    $p = $q;
    $q = $r;
}
say $p;
# The primes below 50, by trial division.
my $primes = "";
CANDIDATE: for (my $n = 2; $n < 50; $n++) {
    for (my $d = 2; $d * $d <= $n; $d++) {
        next CANDIDATE if $n % $d == 0;
    }
    $primes .= " " if length $primes;
    $primes .= $n;
}
say $primes;
# Fibonacci numbers, as far as an Int holds them.
my $f = 0;
my $g = 1;
my $count = 0;
while ($g <= 4660046610375530309) {
    my $next = $f + $g;
    $f = $g;
    $g = $next;
    $count++;
}
say $count . ": " . $g;
# The Collatz sequence from 27: how long, and how high.
my $c = 27;
my $steps = 0;
my $peak = $c;
until ($c == 1) {
    $c = $c % 2 ? 3 * $c + 1 : $c / 2;
    $peak = $c if $c > $peak;
    $steps++;
}
say $steps . " steps, peak " . $peak;
# A string, backwards.
my $word = "stressed";
my $back = "";
for (my $at = length($word) - 1; $at >= 0; $at--) {
    $back .= substr($word, $at, 1);
}
say $back;
# A number in binary.
my $number = 2026;
my $bits = "";
while ($number > 0) {
    $bits = $number % 2 . $bits;
    $number = ($number - $number % 2) / 2;
}
say $bits;
# How many times a letter is in a string.
my $text = "the quick brown fox jumps over the lazy dog";
my $found = 0;
my $from = 0;
while (($from = index($text, "o", $from)) >= 0) {
    $found++;
    $from++;
}
say $found;
# A square of stars, hollow.
for (my $row = 0; $row < 4; $row++) {
    my $line = "";
    for (my $col = 0; $col < 6; $col++) {
        $line .= $row == 0 || $row == 3 || $col == 0 || $col == 5 ? "*" : " ";
    }
    say $line;
}
# Powers of two, until one would not be an exact Int.
my $power = 1;
my $exponent = 0;
while ($power < 4611686018427387904) {
    $power *= 2;
    $exponent++;
}
say "2 ** " . $exponent . " is " . $power;
# The square root of 2, by Newton's method.
my $guess = 1.0;
my $rounds = 0;
while (($guess * $guess - 2) ** 2 > 1e-20) {
    $guess = ($guess + 2 / $guess) / 2;
    $rounds++;
    last if $rounds > 20;
}
say $rounds . " rounds: " . $guess;
