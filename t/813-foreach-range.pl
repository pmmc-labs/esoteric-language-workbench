# model: t/models/each.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my $line201 = "";
my $n201 = 3;
sub limit201() {
    return $n201;
}
$line201 = "";
for my $i ((1 .. 5)) {
    $line201 .= ($i . ' ');
}
say($line201);
$line201 = "";
for my $i ((3 .. 1)) {
    $line201 .= ($i . ' ');
}
say($line201);
$line201 = "";
for my $i ((0 .. 0)) {
    $line201 .= ($i . ' ');
}
say($line201);
$line201 = "";
for my $i (((-2) .. 2)) {
    $line201 .= ($i . ' ');
}
say($line201);
$line201 = "";
for my $i ((1.9 .. 4.1)) {
    $line201 .= ($i . ' ');
}
say($line201);
$line201 = "";
for my $i (((-1.9) .. 1.9)) {
    $line201 .= ($i . ' ');
}
say($line201);
$line201 = "";
for my $i ((false .. true)) {
    $line201 .= ($i . ' ');
}
say($line201);
$line201 = "";
for my $i ((1 .. $n201)) {
    $line201 .= ($i . ' ');
}
say($line201);
$line201 = "";
for my $i ((($n201 - 1) .. ($n201 * 2))) {
    $line201 .= ($i . ' ');
}
say($line201);
$line201 = "";
for my $i ((9223372036854775805 .. 9223372036854775807)) {
    $line201 .= ($i . ' ');
}
say($line201);
$line201 = "";
for my $i (((-9223372036854775295) .. (-9223372036854775294))) {
    $line201 .= ($i . ' ');
}
say($line201);
$line201 = "";
for my $i ((5 .. 4)) {
    $line201 .= ($i . ' ');
}
say($line201);
$line201 = "";
for my $i (((-0.0) .. 1)) {
    $line201 .= ($i . ' ');
}
say($line201);
$line201 = "";
for my $i ((1 .. limit201())) {
    $n201 = 10;
    $line201 .= $i;
}
say($line201);
$line201 = "";
for my $i ((1 .. 9)) {
    next if $i % 2;
    last if $i > 6;
    $line201 .= $i;
}
say($line201);
my $c201 = 0;
for my $i ((1 .. 200000)) {
    $c201++;
}
say($c201);
$line201 = "";
for my $i ((1 .. 5000000000)) {
    last if $i == 4;
    $line201 .= $i;
}
say($line201);
$line201 = "";
for my $i ((1 .. 3)) {
    for my $j (($i .. 3)) {
        $line201 .= (($i . $j) . ' ');
    }
}
say($line201);
