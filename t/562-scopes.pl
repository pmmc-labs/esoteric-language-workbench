# A my is seen from the statement after its own to the end of its block;
# an inner one hides an outer one and ends with its block; a my in the
# test of an if is seen in that if's blocks and later tests, and no
# further (D56, T58).
use v5.42;
my $x = 1;
{
    say $x;
    my $x = $x + 10;
    say $x;
    {
        my $x = $x + 100;
        say $x;
        $x++;
        say $x;
    }
    say $x;
    $x++;
}
say $x;
{
    $x = 2;
    my $y = "inner";
    say $y;
}
say $x;
{
    my $y;
    say defined $y ? "defined" : "undef";
    $y = "another";
    say $y;
}
my $y = "outer";
if (my $z = $x + 5) {
    say $z;
    my $y = "in the if";
    say $y;
    $z++;
} elsif ($z) {
    say "not reached";
}
say $y;
if (my $z = $x - 2) {
    say "not reached";
} elsif (my $w = $z + 3) {
    say $z . "|" . $w;
    $z = "set in the elsif";
    my $x = "hidden";
    say $x;
} else {
    say "not reached";
}
say $x;
if (my $z = 0 * $x) {
    say "not reached";
} elsif (my $w = $z) {
    say "not reached";
} else {
    say $z . "|" . $w;
    my $z = "else's own";
    say $z;
}
unless (my $z = $x - 2) {
    say "unless: " . $z;
}
my $n = 0;
if (($n = $n + 1) > 0) {
    my $n = $n * 100;
    say $n;
    if ($n > 50) {
        my $n = $n + 1;
        say $n;
    }
    say $n;
}
say $n;
my $t = 5;
{
    {
        {
            $t = $t * 2;
        }
        my $t = "shadow";
        say $t;
    }
    say $t;
}
