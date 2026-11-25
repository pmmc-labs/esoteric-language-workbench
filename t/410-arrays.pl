# model: t/models/list.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my @a1 = (0, 1, (-7), 0.5, 3.0, "", '0', 'ab', ' 3 ', true, false, (undef));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a1) {
        $dump_s .= (defined($a1[$dump_i]) ? (('<' . $a1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a1) . ':') . $dump_s);
}
my @b1 = (@a1);
$b1[0] = 9;
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @b1) {
        $dump_s .= (defined($b1[$dump_i]) ? (('<' . $b1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@b1) . ':') . $dump_s);
}
say($a1[0]);
my @e1;
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @e1) {
        $dump_s .= (defined($e1[$dump_i]) ? (('<' . $e1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@e1) . ':') . $dump_s);
}
my @one1 = (5);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @one1) {
        $dump_s .= (defined($one1[$dump_i]) ? (('<' . $one1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@one1) . ':') . $dump_s);
}
my @none1 = ();
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @none1) {
        $dump_s .= (defined($none1[$dump_i]) ? (('<' . $none1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@none1) . ':') . $dump_s);
}
@a1 = (1, 2);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a1) {
        $dump_s .= (defined($a1[$dump_i]) ? (('<' . $a1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a1) . ':') . $dump_s);
}
@a1 = ();
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a1) {
        $dump_s .= (defined($a1[$dump_i]) ? (('<' . $a1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a1) . ':') . $dump_s);
}
@a1 = ((undef));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a1) {
        $dump_s .= (defined($a1[$dump_i]) ? (('<' . $a1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a1) . ':') . $dump_s);
}
my @t1 = (1, 2, 3);
@t1 = (@t1, 4);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @t1) {
        $dump_s .= (defined($t1[$dump_i]) ? (('<' . $t1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@t1) . ':') . $dump_s);
}
@t1 = (@t1, @t1);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @t1) {
        $dump_s .= (defined($t1[$dump_i]) ? (('<' . $t1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@t1) . ':') . $dump_s);
}
my @a2 = (10, 20, 30);
say(defined($a2[0]) ? (('[' . $a2[0]) . ']') : 'undef');
say(defined($a2[1]) ? (('[' . $a2[1]) . ']') : 'undef');
say(defined($a2[2]) ? (('[' . $a2[2]) . ']') : 'undef');
say(defined($a2[3]) ? (('[' . $a2[3]) . ']') : 'undef');
say(defined($a2[4]) ? (('[' . $a2[4]) . ']') : 'undef');
say(defined($a2[(-1)]) ? (('[' . $a2[(-1)]) . ']') : 'undef');
say(defined($a2[(-2)]) ? (('[' . $a2[(-2)]) . ']') : 'undef');
say(defined($a2[(-3)]) ? (('[' . $a2[(-3)]) . ']') : 'undef');
say(defined($a2[(-4)]) ? (('[' . $a2[(-4)]) . ']') : 'undef');
say(defined($a2[(-5)]) ? (('[' . $a2[(-5)]) . ']') : 'undef');
say(defined($a2[1.9]) ? (('[' . $a2[1.9]) . ']') : 'undef');
say(defined($a2[(-1.9)]) ? (('[' . $a2[(-1.9)]) . ']') : 'undef');
say(defined($a2[0.5]) ? (('[' . $a2[0.5]) . ']') : 'undef');
say(defined($a2[(-0.5)]) ? (('[' . $a2[(-0.5)]) . ']') : 'undef');
say(defined($a2['2']) ? (('[' . $a2['2']) . ']') : 'undef');
say(defined($a2[' 1 ']) ? (('[' . $a2[' 1 ']) . ']') : 'undef');
say(defined($a2['-1']) ? (('[' . $a2['-1']) . ']') : 'undef');
say(defined($a2[true]) ? (('[' . $a2[true]) . ']') : 'undef');
say(defined($a2[false]) ? (('[' . $a2[false]) . ']') : 'undef');
say(defined($a2[1.0]) ? (('[' . $a2[1.0]) . ']') : 'undef');
say(defined($a2[9223372036854775807]) ? (('[' . $a2[9223372036854775807]) . ']') : 'undef');
say(defined($a2[(-9223372036854775807 - 1)]) ? (('[' . $a2[(-9223372036854775807 - 1)]) . ']') : 'undef');
say(defined($a2[2147483648]) ? (('[' . $a2[2147483648]) . ']') : 'undef');
say(defined($a2[(-2147483648)]) ? (('[' . $a2[(-2147483648)]) . ']') : 'undef');
say(defined($a2[1099511627776]) ? (('[' . $a2[1099511627776]) . ']') : 'undef');
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a2) {
        $dump_s .= (defined($a2[$dump_i]) ? (('<' . $a2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a2) . ':') . $dump_s);
}
say($#a2);
say(scalar(@a2));
my @e2;
say($#e2);
say(defined($e2[0]) ? (('[' . $e2[0]) . ']') : 'undef');
say(defined($e2[(-1)]) ? (('[' . $e2[(-1)]) . ']') : 'undef');
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @e2) {
        $dump_s .= (defined($e2[$dump_i]) ? (('<' . $e2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@e2) . ':') . $dump_s);
}
my $i2 = 1;
say($a2[$i2]);
say($a2[$i2 + 1]);
say($a2[$#a2]);
say($a2[@a2 - 1]);
say(defined($a2[@a2]) ? (('[' . $a2[@a2]) . ']') : 'undef');
say($a2[$a2[0] - 9]);
