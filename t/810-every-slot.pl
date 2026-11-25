# Every slot of a frame is a root, the last ones too (D66). Each case
# holds a string that was made as the program ran in a slot the others
# don't reach, and reads it after more strings have been made: under a
# collection at every allocation, a slot the collector was not shown is a
# string read after it was collected.
use v5.42;
my $p = "p";
my $q = "q";
my $r = "r";
my $s = "s";
# The statement of this file with the most temporaries, thirteen, and the
# last of them is read by an operation that allocates: so the last slot of
# the frame holds a made string across a collection.
$s .= ((($p . "a") . ($q . "b")) . (($r . "c") . ($p . "d"))) . ((($q . "e") . ($r . "f")) . ("g" . $p));
say $s;
$s = length(($p . "a") . ($q . "b")) . (($r . "c") . ($s . "d"));
say $s;
# A variable holds what a temporary held too, until the temporary is used
# again: so three more statements that make strings, and then the read.
my $v = $p . "v";
my $w = $q . "1";
$w = $q . "2";
$w = $q . "3";
say $v . $w;
# The deepest variable of the file, and the first.
my $first = $p . "first";
{
    my $one = $p . "1";
    {
        my $two = $p . "2";
        {
            my $three = $p . "3";
            {
                my $deepest = $p . "deepest";
                $w = ($q . "x") . ($q . "y");
                $w = ($q . "z") . ($w . "!");
                say $deepest . $three . $two . $one . $first;
            }
        }
    }
}
# A slot used by one block and then by the next.
{
    my $here = $p . "here";
    $w = $q . "4";
    $w = $q . "5";
    say $here;
}
{
    my $there = $q . "there";
    $w = $q . "6";
    $w = $q . "7";
    say $there;
}
# The value of a loop's test, a `my` in it, and what `||` and `? :` give.
my $i = 0;
while ((my $t = $p . $i) ne "p3") {
    $w = $q . $i;
    $w = $w . $w;
    say $t . $w;
    $i++;
}
$w = ($p . "left" || $q . "right") . ($i ? $p . "then" : $q . "else") . ($q . "end");
say $w;
for (my $k = $p . "k"; length($k) < 5; $k .= $q . "k") {
    $w = $k . $k;
    $w = $w . $w;
    say $k;
}
say $first . $v . $s;
