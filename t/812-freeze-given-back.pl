# model: t/models/each.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my @a101 = (1, 2, 3);
for my $x (@a101) {
    my $c = $x;
}
push(@a101, 0);
$a101[0] = ($a101[0] + 1);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a101) {
        $dump_s .= (defined($a101[$dump_i]) ? (('<' . $a101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a101) . ':') . $dump_s);
}
for my $x (@a101) {
    last if $x == 2;
}
push(@a101, 0);
$a101[0] = ($a101[0] + 1);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a101) {
        $dump_s .= (defined($a101[$dump_i]) ? (('<' . $a101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a101) . ':') . $dump_s);
}
OUT: for my $x (@a101) {
    for my $y (@a101) {
        last OUT if $y == 2;
    }
}
push(@a101, 0);
$a101[0] = ($a101[0] + 1);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a101) {
        $dump_s .= (defined($a101[$dump_i]) ? (('<' . $a101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a101) . ':') . $dump_s);
}
OUT: for my $x (@a101) {
    for my $y (@a101) {
        next OUT if $y == 2;
    }
}
push(@a101, 0);
$a101[0] = ($a101[0] + 1);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a101) {
        $dump_s .= (defined($a101[$dump_i]) ? (('<' . $a101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a101) . ':') . $dump_s);
}
my $k101 = 0;
W: while (($k101++) < 2) {
    for my $x (@a101) {
        next W if true;
    }
}
push(@a101, 0);
$a101[0] = ($a101[0] + 1);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a101) {
        $dump_s .= (defined($a101[$dump_i]) ? (('<' . $a101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a101) . ':') . $dump_s);
}
sub one101() {
    for my $x (@a101) {
        return $x;
    }
    return 0;
}
sub two101() {
    for my $x (@a101) {
        for my $y (@a101) {
            return $y;
        }
    }
    return 0;
}
say(one101());
push(@a101, 0);
$a101[0] = ($a101[0] + 1);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a101) {
        $dump_s .= (defined($a101[$dump_i]) ? (('<' . $a101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a101) . ':') . $dump_s);
}
say(two101());
push(@a101, 0);
$a101[0] = ($a101[0] + 1);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a101) {
        $dump_s .= (defined($a101[$dump_i]) ? (('<' . $a101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a101) . ':') . $dump_s);
}
for my $x ($a101[0]) {
    for my $y (@a101) {
        my $c = $y;
    }
    for my $y (@a101[0, 1]) {
        my $c = $y;
    }
}
push(@a101, 0);
$a101[0] = ($a101[0] + 1);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a101) {
        $dump_s .= (defined($a101[$dump_i]) ? (('<' . $a101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a101) . ':') . $dump_s);
}
sub walk101() {
    my $n = 0;
    for my $x (@a101) {
        $n++;
    }
    return $n;
}
say(walk101());
push(@a101, 0);
$a101[0] = ($a101[0] + 1);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a101) {
        $dump_s .= (defined($a101[$dump_i]) ? (('<' . $a101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a101) . ':') . $dump_s);
}
my $n101 = scalar(@a101);
for my $i ((0 .. ($n101 - 1))) {
    $a101[$i] *= 2;
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a101) {
        $dump_s .= (defined($a101[$dump_i]) ? (('<' . $a101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a101) . ':') . $dump_s);
}
