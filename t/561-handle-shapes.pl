# A variable first after say or print, a blank, and an operator: perl
# takes the variable for a file handle only when what follows the blank
# could begin a value (T111). None of these could.
use v5.42;
my $x = 7;
say $x - 1;
say $x-1;
say $x -= 1;
say $x += 1;
say $x //2;
say $x /= 2;
say $x *2;
say $x * 2;
say $x %2;
say $x <2;
say $x <=>2;
say $x ==3.5;
say $x !=3.5;
say $x ."a";
say $x . 5;
say $x **2;
say $x ?1 : 2;
say $x x 2;
say $x x= 2;
say $x;
$x = 7;
say $x if $x -1;
say $x lt 4;
say $x
  - 1;
say $x # the comment is nothing
  + 1;
$x = 7;
say 1 + $x -1;
say -$x -1;
say +$x -1;
say($x - 1);
say($x-1);
say(-$x -1);
say((($x)) - 1);
print $x - 1;
print "\n";
my $y = $x -1;
say $y;
$y = $x +1;
say $y;
say "" . $x -1;
say $x++ -1;
say $x-- +1;
say $x++ /2;
say $x++ .5;
