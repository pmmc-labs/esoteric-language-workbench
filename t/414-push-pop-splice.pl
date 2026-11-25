# model: t/models/list.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my @a401;
say(push(@a401, 1, 2));
say(push(@a401, 3));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a401) {
        $dump_s .= (defined($a401[$dump_i]) ? (('<' . $a401[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a401) . ':') . $dump_s);
}
say(pop(@a401));
say(shift(@a401));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a401) {
        $dump_s .= (defined($a401[$dump_i]) ? (('<' . $a401[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a401) . ':') . $dump_s);
}
say(pop(@a401));
say(defined(pop(@a401)) ? (('[' . pop(@a401)) . ']') : 'undef');
say(defined(shift(@a401)) ? (('[' . shift(@a401)) . ']') : 'undef');
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a401) {
        $dump_s .= (defined($a401[$dump_i]) ? (('<' . $a401[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a401) . ':') . $dump_s);
}
say(unshift(@a401, 5, 6));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a401) {
        $dump_s .= (defined($a401[$dump_i]) ? (('<' . $a401[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a401) . ':') . $dump_s);
}
my @b401 = (7, 8);
push(@a401, @b401, 9);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a401) {
        $dump_s .= (defined($a401[$dump_i]) ? (('<' . $a401[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a401) . ':') . $dump_s);
}
push(@a401, @a401);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a401) {
        $dump_s .= (defined($a401[$dump_i]) ? (('<' . $a401[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a401) . ':') . $dump_s);
}
unshift(@a401, @b401, (0, 0));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a401) {
        $dump_s .= (defined($a401[$dump_i]) ? (('<' . $a401[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a401) . ':') . $dump_s);
}
say(pop(@a401) - pop(@a401));
say(shift(@a401) . shift(@a401));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a401) {
        $dump_s .= (defined($a401[$dump_i]) ? (('<' . $a401[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a401) . ':') . $dump_s);
}
push(@a401, (1 .. 3), (('r') x 2), @b401[1, 0]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a401) {
        $dump_s .= (defined($a401[$dump_i]) ? (('<' . $a401[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a401) . ':') . $dump_s);
}
push(@a401, ());
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a401) {
        $dump_s .= (defined($a401[$dump_i]) ? (('<' . $a401[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a401) . ':') . $dump_s);
}
push(@a401, (undef));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a401) {
        $dump_s .= (defined($a401[$dump_i]) ? (('<' . $a401[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a401) . ':') . $dump_s);
}
push(@a401, scalar(@a401));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a401) {
        $dump_s .= (defined($a401[$dump_i]) ? (('<' . $a401[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a401) . ':') . $dump_s);
}
my $n401 = push(@a401, 0) + 1;
say($n401);
while (@a401) {
    pop(@a401);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a401) {
        $dump_s .= (defined($a401[$dump_i]) ? (('<' . $a401[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a401) . ':') . $dump_s);
}
push(@a401, 1, 2, 3);
push(@a401, shift(@a401));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a401) {
        $dump_s .= (defined($a401[$dump_i]) ? (('<' . $a401[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a401) . ':') . $dump_s);
}
unshift(@a401, pop(@a401));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a401) {
        $dump_s .= (defined($a401[$dump_i]) ? (('<' . $a401[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a401) . ':') . $dump_s);
}
my @a402;
my @r402;
@a402 = (0, 1, 2, 3, 4, 5);
@r402 = (splice(@a402, 1, 2));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r402) {
        $dump_s .= (defined($r402[$dump_i]) ? (('<' . $r402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r402) . ':') . $dump_s);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a402) {
        $dump_s .= (defined($a402[$dump_i]) ? (('<' . $a402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a402) . ':') . $dump_s);
}
@a402 = (0, 1, 2, 3, 4, 5);
@r402 = (splice(@a402, 2));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r402) {
        $dump_s .= (defined($r402[$dump_i]) ? (('<' . $r402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r402) . ':') . $dump_s);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a402) {
        $dump_s .= (defined($a402[$dump_i]) ? (('<' . $a402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a402) . ':') . $dump_s);
}
@a402 = (0, 1, 2, 3, 4, 5);
@r402 = (splice(@a402, 1, 0, 7, 8));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r402) {
        $dump_s .= (defined($r402[$dump_i]) ? (('<' . $r402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r402) . ':') . $dump_s);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a402) {
        $dump_s .= (defined($a402[$dump_i]) ? (('<' . $a402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a402) . ':') . $dump_s);
}
@a402 = (0, 1, 2, 3, 4, 5);
@r402 = (splice(@a402, (-1)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r402) {
        $dump_s .= (defined($r402[$dump_i]) ? (('<' . $r402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r402) . ':') . $dump_s);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a402) {
        $dump_s .= (defined($a402[$dump_i]) ? (('<' . $a402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a402) . ':') . $dump_s);
}
@a402 = (0, 1, 2, 3, 4, 5);
@r402 = (splice(@a402, 0, (-1)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r402) {
        $dump_s .= (defined($r402[$dump_i]) ? (('<' . $r402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r402) . ':') . $dump_s);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a402) {
        $dump_s .= (defined($a402[$dump_i]) ? (('<' . $a402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a402) . ':') . $dump_s);
}
@a402 = (0, 1, 2, 3, 4, 5);
@r402 = (splice(@a402));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r402) {
        $dump_s .= (defined($r402[$dump_i]) ? (('<' . $r402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r402) . ':') . $dump_s);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a402) {
        $dump_s .= (defined($a402[$dump_i]) ? (('<' . $a402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a402) . ':') . $dump_s);
}
@a402 = (0, 1, 2, 3, 4, 5);
@r402 = (splice(@a402, 0));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r402) {
        $dump_s .= (defined($r402[$dump_i]) ? (('<' . $r402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r402) . ':') . $dump_s);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a402) {
        $dump_s .= (defined($a402[$dump_i]) ? (('<' . $a402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a402) . ':') . $dump_s);
}
@a402 = (0, 1, 2, 3, 4, 5);
@r402 = (splice(@a402, 6));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r402) {
        $dump_s .= (defined($r402[$dump_i]) ? (('<' . $r402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r402) . ':') . $dump_s);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a402) {
        $dump_s .= (defined($a402[$dump_i]) ? (('<' . $a402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a402) . ':') . $dump_s);
}
@a402 = (0, 1, 2, 3, 4, 5);
@r402 = (splice(@a402, 6, 0));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r402) {
        $dump_s .= (defined($r402[$dump_i]) ? (('<' . $r402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r402) . ':') . $dump_s);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a402) {
        $dump_s .= (defined($a402[$dump_i]) ? (('<' . $a402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a402) . ':') . $dump_s);
}
@a402 = (0, 1, 2, 3, 4, 5);
@r402 = (splice(@a402, 3, 1));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r402) {
        $dump_s .= (defined($r402[$dump_i]) ? (('<' . $r402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r402) . ':') . $dump_s);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a402) {
        $dump_s .= (defined($a402[$dump_i]) ? (('<' . $a402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a402) . ':') . $dump_s);
}
@a402 = (0, 1, 2, 3, 4, 5);
@r402 = (splice(@a402, 0, 99));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r402) {
        $dump_s .= (defined($r402[$dump_i]) ? (('<' . $r402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r402) . ':') . $dump_s);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a402) {
        $dump_s .= (defined($a402[$dump_i]) ? (('<' . $a402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a402) . ':') . $dump_s);
}
@a402 = (0, 1, 2, 3, 4, 5);
@r402 = (splice(@a402, 1, (-9)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r402) {
        $dump_s .= (defined($r402[$dump_i]) ? (('<' . $r402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r402) . ':') . $dump_s);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a402) {
        $dump_s .= (defined($a402[$dump_i]) ? (('<' . $a402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a402) . ':') . $dump_s);
}
@a402 = (0, 1, 2, 3, 4, 5);
@r402 = (splice(@a402, (-6), 2));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r402) {
        $dump_s .= (defined($r402[$dump_i]) ? (('<' . $r402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r402) . ':') . $dump_s);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a402) {
        $dump_s .= (defined($a402[$dump_i]) ? (('<' . $a402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a402) . ':') . $dump_s);
}
@a402 = (0, 1, 2, 3, 4, 5);
@r402 = (splice(@a402, 2, 2, 'x'));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r402) {
        $dump_s .= (defined($r402[$dump_i]) ? (('<' . $r402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r402) . ':') . $dump_s);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a402) {
        $dump_s .= (defined($a402[$dump_i]) ? (('<' . $a402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a402) . ':') . $dump_s);
}
@a402 = (0, 1, 2, 3, 4, 5);
@r402 = (splice(@a402, 2, 0, (1, 2), 'y'));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r402) {
        $dump_s .= (defined($r402[$dump_i]) ? (('<' . $r402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r402) . ':') . $dump_s);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a402) {
        $dump_s .= (defined($a402[$dump_i]) ? (('<' . $a402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a402) . ':') . $dump_s);
}
@a402 = (0, 1, 2, 3, 4, 5);
@r402 = (splice(@a402, 1.9, 1.9));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r402) {
        $dump_s .= (defined($r402[$dump_i]) ? (('<' . $r402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r402) . ':') . $dump_s);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a402) {
        $dump_s .= (defined($a402[$dump_i]) ? (('<' . $a402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a402) . ':') . $dump_s);
}
@a402 = (0, 1, 2, 3, 4, 5);
@r402 = (splice(@a402, '1', '2'));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r402) {
        $dump_s .= (defined($r402[$dump_i]) ? (('<' . $r402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r402) . ':') . $dump_s);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a402) {
        $dump_s .= (defined($a402[$dump_i]) ? (('<' . $a402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a402) . ':') . $dump_s);
}
@a402 = (0, 1, 2, 3, 4, 5);
@r402 = (splice(@a402, 0, 0));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r402) {
        $dump_s .= (defined($r402[$dump_i]) ? (('<' . $r402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r402) . ':') . $dump_s);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a402) {
        $dump_s .= (defined($a402[$dump_i]) ? (('<' . $a402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a402) . ':') . $dump_s);
}
@a402 = (0, 1, 2, 3, 4, 5);
@r402 = (splice(@a402, (-2), (-1), 'z'));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r402) {
        $dump_s .= (defined($r402[$dump_i]) ? (('<' . $r402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r402) . ':') . $dump_s);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a402) {
        $dump_s .= (defined($a402[$dump_i]) ? (('<' . $a402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a402) . ':') . $dump_s);
}
@a402 = (0, 1, 2, 3, 4, 5);
@r402 = (splice(@a402, 5, 1, 'at the end'));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r402) {
        $dump_s .= (defined($r402[$dump_i]) ? (('<' . $r402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r402) . ':') . $dump_s);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a402) {
        $dump_s .= (defined($a402[$dump_i]) ? (('<' . $a402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a402) . ':') . $dump_s);
}
@a402 = (0, 1, 2, 3, 4, 5);
@r402 = (splice(@a402, 0, 6, ()));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r402) {
        $dump_s .= (defined($r402[$dump_i]) ? (('<' . $r402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r402) . ':') . $dump_s);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a402) {
        $dump_s .= (defined($a402[$dump_i]) ? (('<' . $a402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a402) . ':') . $dump_s);
}
@a402 = (0, 1, 2, 3, 4, 5);
@r402 = (splice(@a402, true, true));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r402) {
        $dump_s .= (defined($r402[$dump_i]) ? (('<' . $r402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r402) . ':') . $dump_s);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a402) {
        $dump_s .= (defined($a402[$dump_i]) ? (('<' . $a402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a402) . ':') . $dump_s);
}
@a402 = (1, 2, 3);
splice(@a402, 1, 1);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a402) {
        $dump_s .= (defined($a402[$dump_i]) ? (('<' . $a402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a402) . ':') . $dump_s);
}
@a402 = (1, 2, 3);
@r402 = (splice(@a402, 0, 1, @a402));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a402) {
        $dump_s .= (defined($a402[$dump_i]) ? (('<' . $a402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a402) . ':') . $dump_s);
}
@a402 = (1, 2, 3);
say(splice(@a402, 0, 2));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a402) {
        $dump_s .= (defined($a402[$dump_i]) ? (('<' . $a402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a402) . ':') . $dump_s);
}
my @e402;
@r402 = (splice(@e402));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r402) {
        $dump_s .= (defined($r402[$dump_i]) ? (('<' . $r402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r402) . ':') . $dump_s);
}
@r402 = (splice(@e402, 0, 0, 1));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @e402) {
        $dump_s .= (defined($e402[$dump_i]) ? (('<' . $e402[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@e402) . ':') . $dump_s);
}
