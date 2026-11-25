# model: t/models/list.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my ($p301, $q301, $r301) = (1, 2, 3);
say(((((defined($p301) ? (('[' . $p301) . ']') : 'undef') . ' ') . (defined($q301) ? (('[' . $q301) . ']') : 'undef')) . ' ') . (defined($r301) ? (('[' . $r301) . ']') : 'undef'));
($p301, $q301, $r301) = (1, 2);
say(((((defined($p301) ? (('[' . $p301) . ']') : 'undef') . ' ') . (defined($q301) ? (('[' . $q301) . ']') : 'undef')) . ' ') . (defined($r301) ? (('[' . $r301) . ']') : 'undef'));
($p301, $q301, $r301) = (1);
say(((((defined($p301) ? (('[' . $p301) . ']') : 'undef') . ' ') . (defined($q301) ? (('[' . $q301) . ']') : 'undef')) . ' ') . (defined($r301) ? (('[' . $r301) . ']') : 'undef'));
($p301, $q301, $r301) = ();
say(((((defined($p301) ? (('[' . $p301) . ']') : 'undef') . ' ') . (defined($q301) ? (('[' . $q301) . ']') : 'undef')) . ' ') . (defined($r301) ? (('[' . $r301) . ']') : 'undef'));
($p301, $q301, $r301) = (1, 2, 3, 4);
say(((((defined($p301) ? (('[' . $p301) . ']') : 'undef') . ' ') . (defined($q301) ? (('[' . $q301) . ']') : 'undef')) . ' ') . (defined($r301) ? (('[' . $r301) . ']') : 'undef'));
($p301, $q301, $r301) = ((7, 8), 9);
say(((((defined($p301) ? (('[' . $p301) . ']') : 'undef') . ' ') . (defined($q301) ? (('[' . $q301) . ']') : 'undef')) . ' ') . (defined($r301) ? (('[' . $r301) . ']') : 'undef'));
($p301, $q301, $r301) = ((4 .. 9));
say(((((defined($p301) ? (('[' . $p301) . ']') : 'undef') . ' ') . (defined($q301) ? (('[' . $q301) . ']') : 'undef')) . ' ') . (defined($r301) ? (('[' . $r301) . ']') : 'undef'));
my @a301 = ('x', 'y', 'z', 'w');
($p301, $q301, $r301) = (@a301);
say(((((defined($p301) ? (('[' . $p301) . ']') : 'undef') . ' ') . (defined($q301) ? (('[' . $q301) . ']') : 'undef')) . ' ') . (defined($r301) ? (('[' . $r301) . ']') : 'undef'));
($p301, undef, $r301) = (@a301);
say(((((defined($p301) ? (('[' . $p301) . ']') : 'undef') . ' ') . (defined($q301) ? (('[' . $q301) . ']') : 'undef')) . ' ') . (defined($r301) ? (('[' . $r301) . ']') : 'undef'));
(undef, undef, $r301) = (1, 2);
say(((((defined($p301) ? (('[' . $p301) . ']') : 'undef') . ' ') . (defined($q301) ? (('[' . $q301) . ']') : 'undef')) . ' ') . (defined($r301) ? (('[' . $r301) . ']') : 'undef'));
($p301) = (@a301);
say(((((defined($p301) ? (('[' . $p301) . ']') : 'undef') . ' ') . (defined($q301) ? (('[' . $q301) . ']') : 'undef')) . ' ') . (defined($r301) ? (('[' . $r301) . ']') : 'undef'));
($p301, @a301) = (1, 2, 3);
say(((((defined($p301) ? (('[' . $p301) . ']') : 'undef') . ' ') . (defined($q301) ? (('[' . $q301) . ']') : 'undef')) . ' ') . (defined($r301) ? (('[' . $r301) . ']') : 'undef'));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a301) {
        $dump_s .= (defined($a301[$dump_i]) ? (('<' . $a301[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a301) . ':') . $dump_s);
}
($p301, @a301) = (1);
say(((((defined($p301) ? (('[' . $p301) . ']') : 'undef') . ' ') . (defined($q301) ? (('[' . $q301) . ']') : 'undef')) . ' ') . (defined($r301) ? (('[' . $r301) . ']') : 'undef'));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a301) {
        $dump_s .= (defined($a301[$dump_i]) ? (('<' . $a301[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a301) . ':') . $dump_s);
}
(@a301) = (5, 6);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a301) {
        $dump_s .= (defined($a301[$dump_i]) ? (('<' . $a301[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a301) . ':') . $dump_s);
}
my ($m301, @rest301) = (@a301, 7);
say($m301);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @rest301) {
        $dump_s .= (defined($rest301[$dump_i]) ? (('<' . $rest301[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@rest301) . ':') . $dump_s);
}
my ($only301) = (9);
say($only301);
my (undef, $second301) = (1, 2);
say($second301);
my ($u301, $w301) = ();
say(defined($u301) ? (('[' . $u301) . ']') : 'undef');
my ($p302, $q302) = (1, 2);
($p302, $q302) = ($q302, $p302);
say(($p302 . ' ') . $q302);
($p302, $q302) = ($q302, ($p302 + $q302));
say(($p302 . ' ') . $q302);
my @a302 = (1, 2, 3);
($a302[0], $a302[2]) = ($a302[2], $a302[0]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a302) {
        $dump_s .= (defined($a302[$dump_i]) ? (('<' . $a302[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a302) . ':') . $dump_s);
}
($a302[0], $a302[1], $a302[2]) = ($a302[1], $a302[2], $a302[0]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a302) {
        $dump_s .= (defined($a302[$dump_i]) ? (('<' . $a302[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a302) . ':') . $dump_s);
}
($p302, @a302) = (@a302, $p302);
say($p302);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a302) {
        $dump_s .= (defined($a302[$dump_i]) ? (('<' . $a302[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a302) . ':') . $dump_s);
}
($a302[0], @a302) = (9, 8, 7);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a302) {
        $dump_s .= (defined($a302[$dump_i]) ? (('<' . $a302[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a302) . ':') . $dump_s);
}
($a302[5], $p302) = (1);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a302) {
        $dump_s .= (defined($a302[$dump_i]) ? (('<' . $a302[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a302) . ':') . $dump_s);
}
say(defined($p302) ? (('[' . $p302) . ']') : 'undef');
($a302[(-1)], $a302[0]) = ('last', 'first');
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a302) {
        $dump_s .= (defined($a302[$dump_i]) ? (('<' . $a302[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a302) . ':') . $dump_s);
}
@a302 = (@a302[1, 0]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a302) {
        $dump_s .= (defined($a302[$dump_i]) ? (('<' . $a302[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a302) . ':') . $dump_s);
}
my @a303 = (1, 2, 3);
my $i303 = 0;
($i303, $a303[$i303]) = (1, 5);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a303) {
        $dump_s .= (defined($a303[$dump_i]) ? (('<' . $a303[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a303) . ':') . $dump_s);
}
say($i303);
@a303 = (1, 2, 3);
$i303 = 0;
($a303[$i303], $i303) = (5, 1);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a303) {
        $dump_s .= (defined($a303[$dump_i]) ? (('<' . $a303[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a303) . ':') . $dump_s);
}
say($i303);
@a303 = (1, 2, 3);
$i303 = 0;
($a303[$i303++], $a303[$i303++]) = ('x', 'y');
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a303) {
        $dump_s .= (defined($a303[$dump_i]) ? (('<' . $a303[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a303) . ':') . $dump_s);
}
