# if, elsif, else, unless and the two modifiers: one block runs, the
# first whose test is true, and the tests after it are not worked out.
use v5.42;
my $n = 0;
if ($n == 0) { say "zero"; }
if ($n) { say "not reached"; } else { say "else"; }
if ($n) { say "not reached"; } elsif ($n == 0) { say "elsif"; } else { say "not reached"; }
if ($n) {
    say "not reached";
} elsif ($n > 0) {
    say "not reached";
} elsif ($n < 0) {
    say "not reached";
} else {
    say "the last else";
}
if (1) { say "first"; } elsif ($n++) { say "not reached"; }
say $n;
if ($n++) { say "not reached"; } elsif ($n++) { say "second test: " . $n; } elsif ($n++) { say "not reached"; }
say $n;
unless ($n) { say "not reached"; }
unless ($n == 5) { say "unless"; }
if ("") { say "not reached"; }
if ("0") { say "not reached"; }
if ("00") { say "00 is true"; }
if ("0.0") { say "0.0 is true"; }
if (0.0) { say "not reached"; }
if (undef) { say "not reached"; }
if (false) { say "not reached"; }
if (true) { say "true"; }
if (" ") { say "a blank is true"; }
if (-0.0) { say "not reached"; }
my $u;
if ($u) { say "not reached"; } else { say "undef is false"; }
if (!$u) { say "not undef"; }
if (not $u) { say "not undef, in a word"; }
if (defined $u) { say "not reached"; }
if ($u // 1) { say "defined-or"; }
if ($n > 1 && $n < 10) { say "and"; }
if ($n > 10 || $n == 2) { say "or"; }
if ($n > 10 or $n == 2) { say "or, in a word"; }
if ($n == 2 xor $n == 3) { say "xor"; }
if ($n == 2 ? 0 : 1) { say "not reached"; }
if (($n)) { say "brackets"; }
if ($n == 2) { if ($n != 3) { if ($n) { say "three deep"; } } }
if ($n == 2) {
    $n = 10;
    if ($n == 2) { say "not reached"; } else { say "changed inside"; }
}
say "modifier" if $n;
say "not reached" if !$n;
say "unless modifier" unless $n == 2;
say "not reached" unless $n;
$n++ if $n == 10;
say $n;
$n-- unless $n == 11;
say $n;
$n = $n * 2 if $n > 5 and $n < 20;
say $n;
$n = undef if $n == 22;
say defined $n ? "defined" : "undef";
$n //= 4 unless defined $n;
say $n;
$n += 1 if ($n);
say $n;
say "a test with a step" if $n++ == 5;
say $n;
say "a test with an assignment" if ($n = $n + 1) == 7;
say(($n > 3) ? "ternary and modifier" : "not reached") if $n;
if ($n) { say "one line"; say "two statements"; }
if ($n) {
    {
        say "a block in an if";
    }
}
{
    if ($n) { say "an if in a block"; }
    say "after it" unless !$n;
}
my $s = "";
if ($n > 100) { $s = "big"; } elsif ($n > 5) { $s = "middling"; } else { $s = "small"; }
say $s;
if (length $s) { say "length"; }
if ($s eq "middling") { say "eq"; }
if (index($s, "dd") > 0) { say "index"; }
