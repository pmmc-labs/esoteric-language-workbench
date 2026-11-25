# How loops are written: what may be left out, where a label may stand,
# what may follow a block, and the forms of last and next. Each line of
# output is what perl prints for the same text.
use v5.42;
my $i = 0;
while ($i < 2) { $i++; } while ($i < 4) { $i++; }
say $i;
while($i<6){$i++;}
say $i;
until($i>=8){$i++;}
say $i;
for(my $k=0;$k<3;$k++){print $k;}
print "\n";
for ( my $k = 0 ; $k < 3 ; $k++ ) { print $k; }
print "\n";
for (;;) { last; }
for ( ; ; ) { last; }
for (;
     ;
     ) { last; }
for ($i = 0; ; ) { last if $i++ > 1; }
say $i;
for (; $i < 6; ) { $i++; }
say $i;
for (;; $i++) { last if $i > 8; }
say $i;
for ($i = 0, my $n = 5; $i < $n; $i++, $n--) { print $i; print $n; }
print "\n";
while ($i) { $i--; }
until ($i) { $i++; }
say $i;
while (0) { }
until (1) { }
for (; 0; ) { }
while ($i++ < 5) { }
say $i;
OUTER:
while ($i < 9) {
    $i++;
    next OUTER;
}
say $i;
A_1: # a comment between a label and its loop
  # and another
  until ($i > 11) { $i++; }
say $i;
LAST: while (1) { last LAST; }
IF: for (;;) { last IF; }
X: while ($i < 14) { X: while (1) { last X; } $i++; }
say $i;
if ($i) { W: while (1) { if ($i) { last W; } } }
if (!$i) { say "not reached"; } else { for (my $k = 0; $k < 2; $k++) { print $k; } print "\n"; }
$i = 0;
$i++ while $i < 3;
say $i;
$i-- until $i <= 0;
say $i;
$i += 2 while $i < 7;
say $i;
say $i-- while $i > 5;
print $i--; print "\n" while 0;
say("x") while $i++ < 5;
say ("y") while $i++ < 7;
say ("z") until $i++ > 7;
$i = undef while defined $i;
say defined $i ? "defined" : "undef";
$i = 0;
while ($i < 10) {
    $i++;
    next if $i < 3;
    next unless $i > 4;
    last if $i == 8;
    last unless $i;
    print $i;
}
print "\n";
while ($i) { last; }
while ($i) { $i = 0; }
say $i;
while ($i < 3) { $i++; if ($i == 2) { next; } elsif ($i == 3) { last; } else { say "one"; } }
say $i;
my $s = "";
for (my $x = 0; $x < 3; $x++) { for (my $y = 0; $y < 3; $y++) { $s .= $x * $y; } $s .= "|"; }
say $s;
my $t = 3;
while ((my $d = $t--) > 0) { print $d; }
print "\n";
until ((my $d = ++$t) >= 3) { print $d; }
print "\n";
while ($t = $i) { last; }
say $t;
