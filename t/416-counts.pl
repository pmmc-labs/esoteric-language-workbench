# model: t/models/list.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my @a601 = (4, 5, 6);
my @e601;
my $n601 = @a601;
say($n601);
$n601 = @e601;
say($n601);
say(defined('x' . @a601) ? (('[' . ('x' . @a601)) . ']') : 'undef');
say(defined(-@a601) ? (('[' . (-@a601)) . ']') : 'undef');
say(defined(@a601 + 1) ? (('[' . (@a601 + 1)) . ']') : 'undef');
say(defined(@a601 * 2) ? (('[' . (@a601 * 2)) . ']') : 'undef');
say(defined(@a601 ** 2) ? (('[' . (@a601 ** 2)) . ']') : 'undef');
say(defined(@a601 % 2) ? (('[' . (@a601 % 2)) . ']') : 'undef');
say(defined(uc(@a601)) ? (('[' . uc(@a601)) . ']') : 'undef');
say(defined(@a601 == 3) ? (('[' . (@a601 == 3)) . ']') : 'undef');
say(defined(@a601 < 5) ? (('[' . (@a601 < 5)) . ']') : 'undef');
say(defined(!@a601) ? (('[' . (!@a601)) . ']') : 'undef');
say(defined(!@e601) ? (('[' . (!@e601)) . ']') : 'undef');
say(defined(@a601 ? 'some' : 'none') ? (('[' . (@a601 ? 'some' : 'none')) . ']') : 'undef');
say(defined(@e601 ? 'some' : 'none') ? (('[' . (@e601 ? 'some' : 'none')) . ']') : 'undef');
say(defined('-' x @a601) ? (('[' . ('-' x @a601)) . ']') : 'undef');
say(defined(@a601 x 2) ? (('[' . (@a601 x 2)) . ']') : 'undef');
say(defined(@a601 . "") ? (('[' . (@a601 . "")) . ']') : 'undef');
say(defined(@a601 . @e601) ? (('[' . (@a601 . @e601)) . ']') : 'undef');
say(defined(@a601 == @e601) ? (('[' . (@a601 == @e601)) . ']') : 'undef');
say(defined(@a601 - 1) ? (('[' . (@a601 - 1)) . ']') : 'undef');
say(defined(@e601 || 7) ? (('[' . (@e601 || 7)) . ']') : 'undef');
say(defined(@a601 && 't') ? (('[' . (@a601 && 't')) . ']') : 'undef');
say(defined(@a601 // 1) ? (('[' . (@a601 // 1)) . ']') : 'undef');
say(defined(substr('abcdef', @a601)) ? (('[' . substr('abcdef', @a601)) . ']') : 'undef');
say(defined($#a601 + 1) ? (('[' . ($#a601 + 1)) . ']') : 'undef');
say(defined(scalar(@a601) - $#a601) ? (('[' . (scalar(@a601) - $#a601)) . ']') : 'undef');
say(defined(@a601 <=> @e601) ? (('[' . (@a601 <=> @e601)) . ']') : 'undef');
say(defined(@a601 eq '3') ? (('[' . (@a601 eq '3')) . ']') : 'undef');
say(defined((+@a601) + 0) ? (('[' . ((+@a601) + 0)) . ']') : 'undef');
$n601 = 0;
$n601 += @a601;
$n601 .= @a601;
say($n601);
$n601 = (@a601 ? @a601 : 0);
say($n601);
if (@a601) {
    say('if');
}
unless (@e601) {
    say('unless');
}
say('mod') if @a601 > 2;
while (@a601 > 1) {
    pop(@a601);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a601) {
        $dump_s .= (defined($a601[$dump_i]) ? (('<' . $a601[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a601) . ':') . $dump_s);
}
until (@a601 >= 3) {
    push(@a601, 0);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a601) {
        $dump_s .= (defined($a601[$dump_i]) ? (('<' . $a601[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a601) . ':') . $dump_s);
}
my @f601 = ((@a601 || (9)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @f601) {
        $dump_s .= (defined($f601[$dump_i]) ? (('<' . $f601[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@f601) . ':') . $dump_s);
}
my @d601 = ((@e601 || (1, 2)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @d601) {
        $dump_s .= (defined($d601[$dump_i]) ? (('<' . $d601[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@d601) . ':') . $dump_s);
}
my @h601 = ((@a601 ? @a601 : @e601));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @h601) {
        $dump_s .= (defined($h601[$dump_i]) ? (('<' . $h601[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@h601) . ':') . $dump_s);
}
my @k601 = ((@a601 && @e601));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @k601) {
        $dump_s .= (defined($k601[$dump_i]) ? (('<' . $k601[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@k601) . ':') . $dump_s);
}
my @m601 = ((@a601 && (1, 2)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @m601) {
        $dump_s .= (defined($m601[$dump_i]) ? (('<' . $m601[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@m601) . ':') . $dump_s);
}
say($a601[@a601 - 1]);
my ($first601) = (@a601);
say($first601);
my @idx601 = (1);
say($a601[@idx601]);
