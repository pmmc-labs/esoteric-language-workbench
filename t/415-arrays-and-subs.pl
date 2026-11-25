# model: t/models/list.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
sub three501($p, $q, $r) {
    return ($p . $q) . $r;
}
sub cnt501($p = '-', $q = '-', $r = '-') {
    return ((defined($p) ? (('[' . $p) . ']') : 'undef') . (defined($q) ? (('[' . $q) . ']') : 'undef')) . (defined($r) ? (('[' . $r) . ']') : 'undef');
}
sub none501() {
    return;
}
my @a501 = (1, 2);
my @e501;
say(three501(@a501, 3));
say(three501(0, @a501));
say(three501(@e501, 1, @a501));
say(cnt501(@e501));
say(cnt501(@a501));
say(cnt501(@a501, 9));
say(cnt501((@a501)[0]));
say(cnt501((@e501)[0]));
say(cnt501(()));
say(cnt501((), 1));
say(cnt501((1 .. 3)));
say(cnt501(@a501[1, 0]));
say(cnt501((('r') x 2)));
say(cnt501($a501[0], $a501[5]));
say(cnt501(scalar(@a501), $#a501));
say(cnt501(none501(), @a501));
say(cnt501((undef), @e501, (undef)));
my @c501 = (none501());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @c501) {
        $dump_s .= (defined($c501[$dump_i]) ? (('<' . $c501[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@c501) . ':') . $dump_s);
}
my @d501 = (1, none501(), 2);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @d501) {
        $dump_s .= (defined($d501[$dump_i]) ? (('<' . $d501[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@d501) . ':') . $dump_s);
}
my ($y501, $z501) = (none501(), 7);
say($y501);
say(defined($z501) ? (('[' . $z501) . ']') : 'undef');
push(@a501, none501());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a501) {
        $dump_s .= (defined($a501[$dump_i]) ? (('<' . $a501[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a501) . ':') . $dump_s);
}
say('[', none501(), ']');
my @one501 = (three501(1, 2, 3));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @one501) {
        $dump_s .= (defined($one501[$dump_i]) ? (('<' . $one501[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@one501) . ':') . $dump_s);
}
my @two501 = (three501(1, 2, 3), cnt501());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @two501) {
        $dump_s .= (defined($two501[$dump_i]) ? (('<' . $two501[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@two501) . ':') . $dump_s);
}
fill502();
my @a502;
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a502) {
        $dump_s .= (defined($a502[$dump_i]) ? (('<' . $a502[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a502) . ':') . $dump_s);
}
my @b502 = (9);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @b502) {
        $dump_s .= (defined($b502[$dump_i]) ? (('<' . $b502[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@b502) . ':') . $dump_s);
}
fill502();
my ($n502, @m502) = ();
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @m502) {
        $dump_s .= (defined($m502[$dump_i]) ? (('<' . $m502[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@m502) . ':') . $dump_s);
}
sub fill502() {
    push(@a502, 1, 2);
    push(@b502, 3);
    push(@m502, 4);
}
sub own502($p) {
    my @mine;
    push(@mine, $p);
    own502(($p - 1)) if $p > 0;
    push(@mine, 'after');
    say(((scalar(@mine) . ':') . $mine[0]) . $mine[1]);
}
own502(2);
sub total502() {
    my $t = 0;
    my $i = 0;
    while ($i < @a502) {
        $t += $a502[$i];
        $i++;
    }
    return $t;
}
say(total502());
$a502[0] = 100;
say(total502());
sub set502($p, $q) {
    $a502[$p] = $q;
}
set502(5, 1);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a502) {
        $dump_s .= (defined($a502[$dump_i]) ? (('<' . $a502[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a502) . ':') . $dump_s);
}
sub len502() {
    return scalar(@a502);
}
say(len502());
