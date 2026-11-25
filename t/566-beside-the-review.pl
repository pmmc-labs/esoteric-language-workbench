# What stands beside each thing the review of step 5 had refused, and is
# fine: perl says nothing of any of these, and each is what it looks like.
use v5.42;
my $t = "t";
my $u = "u";
my $x = "a";
my $z = "1";
$t .= ($u .= $x);
say $t . "|" . $u;
$t = $t . ($u = $x . $z);
say $t . "|" . $u;
$t .= ($u = $x . $z) . "b";
say $t . "|" . $u;
$t .= "b" . ($u = $z . $x);
say $t . "|" . $u;
$t .= ($u = $x x 2);
say $t . "|" . $u;
$t .= ($u = $x);
say $t . "|" . $u;
$t = "t";
$t .= ($u = $x . $z) x 1;
say $t . "|" . $u;
my $n = 5;
my $m = 2;
my $r =-$m;
say $r;
$r = -$m;
say $r;
$r = - $m;
say $r;
$r=-$m;
say $r;
$r +=- 1;
say $r;
$r -=+ 1;
say $r;
say $n ==- 5;
$r =
  -$m;
say $r;
say("a") if $n;
say ("b") if $n;
say ("c") unless !$n;
say substr("abcdef", $n -1);
say substr("abcdef", $n -4, $m -1);
say index("abcabc", "c", $m +1);
say substr($n - 1, 0);
say substr($n-1, 0);
say index($n . 5, "5");
say length $n -1;
if ($n = $m && 0) { say "not reached"; }
say $n;
if ($n = $m || 5) { say $n; }
$n = 0;
if ($n = $m ? 1 : 0) { say $n; }
# A name of 251 characters, the longest perl takes.
my $vaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa = 251;
say $vaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa;
