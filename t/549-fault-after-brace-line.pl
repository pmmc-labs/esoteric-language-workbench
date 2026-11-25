# kind: fault
# A statement that starts on the line a block ends on is at that line:
# perl warns of this undef at line 9.
use v5.42;
my $u;
my $n = 0;
if ($n) { say "not reached"; }
else {
    say "else"; } $n = $u
  + 1;
