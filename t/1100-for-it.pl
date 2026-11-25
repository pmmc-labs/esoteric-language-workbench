# model: t/models/it.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my @a1 = (1, 2, 3);
my @e1;
my $line1 = "";
sub two1() {
    return ('p', 'q');
}
sub none1() {
    return;
}
$line1 = "";
for (@a1) {
    $line1 .= (defined($_) ? (('<' . $_) . '>') : 'undef');
}
say($line1);
$line1 = "";
for (1, 2, 3) {
    $line1 .= (defined($_) ? (('<' . $_) . '>') : 'undef');
}
say($line1);
$line1 = "";
for (@e1) {
    $line1 .= (defined($_) ? (('<' . $_) . '>') : 'undef');
}
say($line1);
$line1 = "";
for (()) {
    $line1 .= (defined($_) ? (('<' . $_) . '>') : 'undef');
}
say($line1);
$line1 = "";
for (@a1, 9, @e1) {
    $line1 .= (defined($_) ? (('<' . $_) . '>') : 'undef');
}
say($line1);
$line1 = "";
for (@a1[2, 0]) {
    $line1 .= (defined($_) ? (('<' . $_) . '>') : 'undef');
}
say($line1);
$line1 = "";
for ((2 .. 5)) {
    $line1 .= (defined($_) ? (('<' . $_) . '>') : 'undef');
}
say($line1);
$line1 = "";
for (0, (1 .. 2)) {
    $line1 .= (defined($_) ? (('<' . $_) . '>') : 'undef');
}
say($line1);
$line1 = "";
for (((@a1) x 2)) {
    $line1 .= (defined($_) ? (('<' . $_) . '>') : 'undef');
}
say($line1);
$line1 = "";
for ($a1[0], $a1[2]) {
    $line1 .= (defined($_) ? (('<' . $_) . '>') : 'undef');
}
say($line1);
$line1 = "";
for (two1(), none1()) {
    $line1 .= (defined($_) ? (('<' . $_) . '>') : 'undef');
}
say($line1);
$line1 = "";
for (reverse(@a1)) {
    $line1 .= (defined($_) ? (('<' . $_) . '>') : 'undef');
}
say($line1);
$line1 = "";
for ((undef), 0, "", true, false, 1.5) {
    $line1 .= (defined($_) ? (('<' . $_) . '>') : 'undef');
}
say($line1);
$line1 = "";
for (scalar(@a1)) {
    $line1 .= (defined($_) ? (('<' . $_) . '>') : 'undef');
}
say($line1);
$line1 = "";
for ((1 ? @a1 : @e1)) {
    $line1 .= (defined($_) ? (('<' . $_) . '>') : 'undef');
}
say($line1);
$line1 = "";
for ((1, (2, (3)))) {
    $line1 .= (defined($_) ? (('<' . $_) . '>') : 'undef');
}
say($line1);
my @a2 = (1, 2, 3);
my @b2 = (10, 20);
my $line2 = "";
for (@a2) {
    $line2 .= (('o' . $_) . ' ');
    for (@b2) {
        $line2 .= (('i' . $_) . ' ');
    }
    $line2 .= (('o' . $_) . ' ');
}
say($line2);
$line2 = "";
for (@a2) {
    for ((1 .. $_)) {
        $line2 .= ($_ . ' ');
    }
}
say($line2);
$line2 = "";
for (@a2) {
    for ($_, ($_ * 10)) {
        $line2 .= ($_ . ' ');
    }
}
say($line2);
$line2 = "";
for (@a2) {
    for my $x (@b2) {
        $line2 .= (($_ . $x) . ' ');
    }
}
say($line2);
$line2 = "";
for my $x (@a2) {
    for (@b2) {
        $line2 .= (($x . $_) . ' ');
    }
}
say($line2);
$line2 = "";
for (@a2) {
    next if $_ == 2;
    $line2 .= ($_ . ' ');
}
say($line2);
$line2 = "";
for (@a2) {
    last if $_ == 2;
    $line2 .= ($_ . ' ');
}
say($line2);
$line2 = "";
OUT: for (@a2) {
    for (@b2) {
        next OUT if $_ == 20;
        $line2 .= ($_ . ' ');
    }
}
say($line2);
$line2 = "";
for (@a2) {
    my $k = 0;
    while ($k < $_) {
        $line2 .= (($_ . $k) . ' ');
        $k++;
    }
}
say($line2);
$line2 = "";
for (@a2) {
    my $c = $_;
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
for (@a2) {
    push(@b2, ($_ * $a2[0]));
    $line2 .= ((scalar(@a2) . $a2[(-1)]) . ' ');
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
my @a3 = (1, 2, 3);
my @b3;
my $n3 = 0;
my $t3 = "";
sub note3($p) {
    $t3 .= ($p . ';');
    return 0;
}
say($_) for (@a3);
say('v' . $_) for (7, @a3);
say($_, $_) for ((1 .. 2));
$n3 += $_ for (@a3, 10);
say($n3);
$n3++ for (@a3);
say($n3);
push(@b3, ($_ * 2), $_) for (@a3);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @b3) {
        $dump_s .= (defined($b3[$dump_i]) ? (('<' . $b3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@b3) . ':') . $dump_s);
}
note3($_) for (reverse(@a3));
say($t3);
$b3[$_] = 0 for ((0 .. 1));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @b3) {
        $dump_s .= (defined($b3[$dump_i]) ? (('<' . $b3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@b3) . ':') . $dump_s);
}
$t3 .= $_ for (());
say($t3);
say('-');
for (@a3) {
    $n3 += $_ for ((1 .. $_));
    say(($_ . ':') . $n3);
}
for my $x (1, 2) {
    say($x . $_) for (@a3);
}
my @a4 = (4, 8, 15);
sub total4() {
    my $t = 0;
    for (@a4) {
        $t += $_;
    }
    return $t;
}
sub find4($p) {
    for (@a4) {
        return $_ if $_ > $p;
    }
    return (-1);
}
sub twice4($p) {
    return $p * 2;
}
sub inner4($p) {
    my $t = 0;
    $t += $_ for ((1 .. $p));
    return $t;
}
sub all4(@v) {
    my $t = "";
    $t .= $_ for (@v);
    return $t;
}
say(total4());
say(find4(5));
say(find4(99));
for (@a4) {
    say(twice4($_));
}
for (1, 2, 3) {
    say(((($_ . ':') . inner4($_)) . ':') . $_);
}
say(all4(@a4, 16));
say(all4());
