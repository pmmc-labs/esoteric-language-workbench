# The concatenations with a change in them that the language takes: the
# change is in an earlier piece than any read of the variable, or it is
# another variable's (D57). perl joins a row of dots as one operation,
# and these are the ones where that makes no difference.
use v5.42;
my $x = 3;
my $y = "a";
say(($x = 5) . $x);
say(($x = 6) . "|" . $x . "|" . $x);
say $x++ . $x;
say $x++ . "|" . $x . "|" . $x;
say ++$x . $x;
say $x-- . $x . $x;
say $x . $y++ if 0;
say $x . ($y = "b");
say $x . ($y = "c") . $y;
say $x . ($y .= "d") . $y . $x;
$x .= $y;
say $x;
$x .= $x;
say $x;
$x = $x . $x;
say $x;
$x = "<" . $x . ">";
say $x;
$x = 1;
$x .= $x . $x;
say $x;
$x .= "a" . "b" . $y;
say $x;
$x = 1;
$y = 2;
my $z = $x . $y . ($x + $y) . $x * $y . ($x - $y);
say $z;
$z = $x++ . $y++ . $x . $y;
say $z;
$z = ($x += 10) . ($y += 20) . $x . $y;
say $z;
$z = "" . ($x = 0) . ($x || "zero") . ($x // "defined");
say $z;
$z = length($x) . ($y = "long") . length($y);
say $z;
$z .= $z x 2;
say $z;
my $u;
$u .= "from nothing";
say $u;
