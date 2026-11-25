# model: t/models/sub.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(fact201(10));
say(fact201(20));
sub fact201($n) {
    return 1 if $n < 2;
    return $n * fact201($n - 1);
}
sub fib202($n) {
    return ($n < 2) ? $n : (fib202($n - 1) + fib202($n - 2));
}
say(fib202(0));
say(fib202(1));
say(fib202(2));
say(fib202(10));
say(fib202(15));
sub even203($n) {
    return ($n == 0) ? true : odd203($n - 1);
}
sub odd203($n) {
    return ($n == 0) ? false : even203($n - 1);
}
say(defined(even203(0)) ? (('[' . even203(0)) . ']') : 'undef');
say(defined(even203(1)) ? (('[' . even203(1)) . ']') : 'undef');
say(defined(even203(2)) ? (('[' . even203(2)) . ']') : 'undef');
say(defined(even203(7)) ? (('[' . even203(7)) . ']') : 'undef');
say(defined(even203(60)) ? (('[' . even203(60)) . ']') : 'undef');
say(defined(even203(97)) ? (('[' . even203(97)) . ']') : 'undef');
sub gcd204($p, $q) {
    return $p unless $q;
    return gcd204($q, $p % $q);
}
say(gcd204(12, 18));
say(gcd204(17, 5));
say(gcd204(0, 9));
say(gcd204(9, 0));
say(gcd204(1071, 462));
sub ack205($p, $q) {
    return $q + 1 if $p == 0;
    return ack205($p - 1, 1) if $q == 0;
    return ack205($p - 1, ack205($p, $q - 1));
}
say(ack205(2, 3));
sub rev206($p) {
    return $p if length($p) < 2;
    return rev206(substr($p, 1)) . substr($p, 0, 1);
}
say(rev206('abcdefg'));
say(rev206(""));
say(rev206('x'));
sub down207($n) {
    my $mine = $n * 10;
    down207($n - 1) if $n > 0;
    say(($n . ':') . $mine);
}
down207(3);
sub depth208($n) {
    return ($n == 0) ? 0 : (1 + depth208($n - 1));
}
say(depth208(98));
say(depth208(98));
sub find209($p) {
    OUT: for (my $i = 0; $i < 4; $i++) {
        my $j = 0;
        while ($j < 4) {
            return ($i . ',') . $j if ($i * $j) == $p;
            next OUT if ($i * $j) > $p;
            $j++;
        }
    }
    return 'none';
}
sub nest209($p) {
    {
        {
            if ($p) {
                return 'in';
            }
        }
    }
    return 'out';
}
sub until209() {
    my $i = 0;
    until (false) {
        $i++;
        return $i if $i > 3;
    }
}
say(find209(0));
say(find209(2));
say(find209(6));
say(find209(9));
say(find209(7));
say(nest209(1));
say(nest209(0));
say(until209());
