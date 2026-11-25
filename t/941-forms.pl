# How a sub and a call may be written (D72, T136, T137, T138, T139).
use v5.42;

sub one() { return 1; }
sub plus ($x, $y) { return $x + $y; }
sub wide
(
    $x,
    $y = 2,     # a comment in a signature
)
{
    return $x * $y;
}
sub tight($x){return $x;}
sub trailing($x, $y,) { return $x - $y; }

say one();
say plus(1, 2);
say plus(1, 2,);
say wide(3);
say wide(3, 4);
say tight(5);
say trailing(9, 4);

# A blank, or a new line, between a name and its bracket: not first
# after say.
my $r = plus (1, 2);
say $r;
$r = plus
    (3, 4);
say $r;
say 1 + plus (1, 2);
say(+(plus (1, 2)));
$r = plus (1, 2) * 3;
say $r;
plus (1, 2);

# A minus and a call, said so that it is one.
sub e($p) { return $p + 10; }
say - e(2);
say -(e(2));
say 5 - e(2);
say -one();

# return is not a function: its brackets are not its arguments'.
sub six() { return (5) + 1; }
say six();
sub seven() { return(5) + 2; }
say seven();
sub negative() { return -1; }
say negative();
sub nothing($c) {
    return unless $c;
    return "something";
}
say nothing(1);
say defined(nothing(0)) ? "defined" : "undef";

# A default finds the file's variable of its own parameter's name, and
# of a later parameter's (T138); a parameter hides the file's.
my $x = 3;
my $y = 10;
sub own($x = $x) { $x++; return $x; }
sub later($p = $y, $y = 2) { return $p . " " . $y; }
say own();
say own(7);
say $x;
say later();
say later(1, 5);

# A label and a sub of one name; a sub named for nothing perl knows.
sub OUTER() { return "sub"; }
my $i = 0;
OUTER: while ($i < 3) {
    $i++;
    next OUTER if $i == 2;
    say $i . OUTER();
}
sub x2() { return "x2"; }
say x2();
sub _($p) { return $p; }
say _(4);
