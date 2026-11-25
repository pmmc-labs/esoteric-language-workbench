use v5.42;
my $x = "a";
sub ch() { $x = "b"; return "c" }
sub id($p) { return $p }
sub dflt($p = ch()) { return $p }
sub deep() { return ch() }
sub r() { return $x . "-" . ch() }
sub d2($p = $x . "-" . ch()) { return $p }
say $x . "-" . id(ch());
$x = "a"; say $x . "-" . (1 + length(ch()));
$x = "a"; say $x . "-" . dflt();
$x = "a"; say $x . "-" . deep();
$x = "a"; say id($x . "-" . ch());
$x = "a"; say r();
$x = "a"; say d2();
$x = "a"; say(($x . "-") . ch());
$x = "a"; say "<" . ($x . "-") . ch();
$x = "a"; say id($x . "-") . ch();
