# model: t/models/each.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my @a1 = (1, 2, 3);
my @e1;
my @b1 = ('p', 'q');
my $line1 = "";
sub none1() {
    return;
}
sub five1() {
    return 5;
}
$line1 = "";
for my $x (@a1) {
    $line1 .= (('<' . (defined($x) ? $x : 'undef')) . '>');
}
say($line1);
$line1 = "";
for my $x (1, 2, 3) {
    $line1 .= (('<' . (defined($x) ? $x : 'undef')) . '>');
}
say($line1);
$line1 = "";
for my $x (@a1, @b1) {
    $line1 .= (('<' . (defined($x) ? $x : 'undef')) . '>');
}
say($line1);
$line1 = "";
for my $x (@e1) {
    $line1 .= (('<' . (defined($x) ? $x : 'undef')) . '>');
}
say($line1);
$line1 = "";
for my $x (@e1, @e1) {
    $line1 .= (('<' . (defined($x) ? $x : 'undef')) . '>');
}
say($line1);
$line1 = "";
for my $x (()) {
    $line1 .= (('<' . (defined($x) ? $x : 'undef')) . '>');
}
say($line1);
$line1 = "";
for my $x (@a1, 9, @e1, 'z') {
    $line1 .= (('<' . (defined($x) ? $x : 'undef')) . '>');
}
say($line1);
$line1 = "";
for my $x (@a1[2, 0]) {
    $line1 .= (('<' . (defined($x) ? $x : 'undef')) . '>');
}
say($line1);
$line1 = "";
for my $x ((@a1, 7)[3, 0]) {
    $line1 .= (('<' . (defined($x) ? $x : 'undef')) . '>');
}
say($line1);
$line1 = "";
for my $x (((@a1) x 2)) {
    $line1 .= (('<' . (defined($x) ? $x : 'undef')) . '>');
}
say($line1);
$line1 = "";
for my $x ($a1[0], $a1[2]) {
    $line1 .= (('<' . (defined($x) ? $x : 'undef')) . '>');
}
say($line1);
$line1 = "";
for my $x (five1(), none1(), five1()) {
    $line1 .= (('<' . (defined($x) ? $x : 'undef')) . '>');
}
say($line1);
$line1 = "";
for my $x (none1()) {
    $line1 .= (('<' . (defined($x) ? $x : 'undef')) . '>');
}
say($line1);
$line1 = "";
for my $x (scalar(@a1)) {
    $line1 .= (('<' . (defined($x) ? $x : 'undef')) . '>');
}
say($line1);
$line1 = "";
for my $x ((1 .. 4), 9) {
    $line1 .= (('<' . (defined($x) ? $x : 'undef')) . '>');
}
say($line1);
$line1 = "";
for my $x (0, (2 .. 3)) {
    $line1 .= (('<' . (defined($x) ? $x : 'undef')) . '>');
}
say($line1);
$line1 = "";
for my $x ((@a1 ? @b1 : @e1)) {
    $line1 .= (('<' . (defined($x) ? $x : 'undef')) . '>');
}
say($line1);
$line1 = "";
for my $x ((@e1 || @b1)) {
    $line1 .= (('<' . (defined($x) ? $x : 'undef')) . '>');
}
say($line1);
$line1 = "";
for my $x ((@a1 || @b1)) {
    $line1 .= (('<' . (defined($x) ? $x : 'undef')) . '>');
}
say($line1);
$line1 = "";
for my $x ((undef), 0, "") {
    $line1 .= (('<' . (defined($x) ? $x : 'undef')) . '>');
}
say($line1);
$line1 = "";
for my $x ((1, (2, (3)))) {
    $line1 .= (('<' . (defined($x) ? $x : 'undef')) . '>');
}
say($line1);
$line1 = "";
for my $x ($#a1) {
    $line1 .= (('<' . (defined($x) ? $x : 'undef')) . '>');
}
say($line1);
$line1 = "";
for my $x ((@a1 + 1)) {
    $line1 .= (('<' . (defined($x) ? $x : 'undef')) . '>');
}
say($line1);
my @a2 = (1, 2, 3);
my @b2 = (10, 20);
my $line2 = "";
for my $x (@a2) {
    for my $y (@a2) {
        $line2 .= (($x . $y) . ' ');
    }
}
say($line2);
$line2 = "";
for my $x (@a2) {
    for my $y (@b2) {
        next if $y == 10;
        $line2 .= (($x . $y) . ' ');
    }
}
say($line2);
$line2 = "";
OUT: for my $x (@a2) {
    for my $y (@a2) {
        next OUT if $y > $x;
        last OUT if $x == 3;
        $line2 .= (($x . $y) . ' ');
    }
}
say($line2);
$line2 = "";
for my $x (@a2) {
    last if $x == 2;
    $line2 .= ($x . ' ');
}
say($line2);
$line2 = "";
for my $x (@a2) {
    next if $x == 2;
    $line2 .= ($x . ' ');
}
say($line2);
$line2 = "";
my $k2 = 0;
while ($k2 < 2) {
    for my $x (@b2) {
        $line2 .= (($k2 . $x) . ' ');
    }
    $k2++;
}
say($line2);
$line2 = "";
for my $x (@b2) {
    my $n = 0;
    while ($n < 2) {
        $line2 .= (($x . $n) . ' ');
        $n++;
    }
}
say($line2);
$line2 = "";
for my $x (@a2) {
    for (my $j = 0; $j < $x; $j++) {
        $line2 .= (($x . $j) . ' ');
    }
}
say($line2);
$line2 = "";
my $x = 'outer';
for my $x (@b2) {
    $line2 .= ($x . ' ');
}
say($line2 . $x);
$line2 = "";
for my $x (@a2) {
    my $c = $x;
    $c *= 10;
    $line2 .= ($c . ' ');
}
say($line2);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a2) {
        $dump_s .= (defined($a2[$dump_i]) ? (('<' . $a2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a2) . ':') . $dump_s);
}
$line2 = "";
for my $x (@a2) {
    push(@b2, ($x * $a2[0]));
    $line2 .= (((scalar(@a2) . $#a2) . $a2[(-1)]) . ' ');
}
say($line2);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @b2) {
        $dump_s .= (defined($b2[$dump_i]) ? (('<' . $b2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@b2) . ':') . $dump_s);
}
my @a3 = (4, 8, 15, 16);
sub find3($w) {
    for my $x (@a3) {
        return $x if $x > $w;
    }
    return (-1);
}
sub pair3($w) {
    for my $x (@a3) {
        for my $y (@a3) {
            return ($x . '+') . $y if ($x + $y) == $w;
        }
    }
    return 'none';
}
sub total3() {
    my $t = 0;
    for my $x (@a3) {
        $t += $x;
    }
    return $t;
}
sub first3() {
    return $a3[0];
}
say(find3(5));
say(find3(100));
say(pair3(23));
say(pair3(7));
say(total3());
for my $x (@a3) {
    say($x + first3());
}
for my $x (total3(), find3(8)) {
    say($x);
}
