# model: t/models/ret.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my @a201 = ('x', 'y', 'z');
my @e201;
my @r201;
sub two201() {
    return (1, 2);
}
sub none201() {
    return;
}
say(('<' . join(',', @a201)) . '>');
say(('<' . join(',', 1, 2, 3)) . '>');
say(('<' . join(',', @e201)) . '>');
say(('<' . join(',', 'only')) . '>');
say(('<' . join(',', @a201, @a201)) . '>');
say(('<' . join(',', 0.5, true, false, "", (-7), 3.0)) . '>');
say(('<' . join(',', two201(), none201(), two201())) . '>');
say(('<' . join("", @a201)) . '>');
say(('<' . join("", 1, 2, 3)) . '>');
say(('<' . join("", @e201)) . '>');
say(('<' . join("", 'only')) . '>');
say(('<' . join("", @a201, @a201)) . '>');
say(('<' . join("", 0.5, true, false, "", (-7), 3.0)) . '>');
say(('<' . join("", two201(), none201(), two201())) . '>');
say(('<' . join(' - ', @a201)) . '>');
say(('<' . join(' - ', 1, 2, 3)) . '>');
say(('<' . join(' - ', @e201)) . '>');
say(('<' . join(' - ', 'only')) . '>');
say(('<' . join(' - ', @a201, @a201)) . '>');
say(('<' . join(' - ', 0.5, true, false, "", (-7), 3.0)) . '>');
say(('<' . join(' - ', two201(), none201(), two201())) . '>');
say(('<' . join(0, @a201)) . '>');
say(('<' . join(0, 1, 2, 3)) . '>');
say(('<' . join(0, @e201)) . '>');
say(('<' . join(0, 'only')) . '>');
say(('<' . join(0, @a201, @a201)) . '>');
say(('<' . join(0, 0.5, true, false, "", (-7), 3.0)) . '>');
say(('<' . join(0, two201(), none201(), two201())) . '>');
say(('<' . join(1.5, @a201)) . '>');
say(('<' . join(1.5, 1, 2, 3)) . '>');
say(('<' . join(1.5, @e201)) . '>');
say(('<' . join(1.5, 'only')) . '>');
say(('<' . join(1.5, @a201, @a201)) . '>');
say(('<' . join(1.5, 0.5, true, false, "", (-7), 3.0)) . '>');
say(('<' . join(1.5, two201(), none201(), two201())) . '>');
say(('<' . join(true, @a201)) . '>');
say(('<' . join(true, 1, 2, 3)) . '>');
say(('<' . join(true, @e201)) . '>');
say(('<' . join(true, 'only')) . '>');
say(('<' . join(true, @a201, @a201)) . '>');
say(('<' . join(true, 0.5, true, false, "", (-7), 3.0)) . '>');
say(('<' . join(true, two201(), none201(), two201())) . '>');
say(('<' . join(false, @a201)) . '>');
say(('<' . join(false, 1, 2, 3)) . '>');
say(('<' . join(false, @e201)) . '>');
say(('<' . join(false, 'only')) . '>');
say(('<' . join(false, @a201, @a201)) . '>');
say(('<' . join(false, 0.5, true, false, "", (-7), 3.0)) . '>');
say(('<' . join(false, two201(), none201(), two201())) . '>');
say(('<' . join(@a201, @a201)) . '>');
say(('<' . join(@a201, 1, 2, 3)) . '>');
say(('<' . join(@a201, @e201)) . '>');
say(('<' . join(@a201, 'only')) . '>');
say(('<' . join(@a201, @a201, @a201)) . '>');
say(('<' . join(@a201, 0.5, true, false, "", (-7), 3.0)) . '>');
say(('<' . join(@a201, two201(), none201(), two201())) . '>');
say(('<' . join($a201[0], @a201)) . '>');
say(('<' . join($a201[0], 1, 2, 3)) . '>');
say(('<' . join($a201[0], @e201)) . '>');
say(('<' . join($a201[0], 'only')) . '>');
say(('<' . join($a201[0], @a201, @a201)) . '>');
say(('<' . join($a201[0], 0.5, true, false, "", (-7), 3.0)) . '>');
say(('<' . join($a201[0], two201(), none201(), two201())) . '>');
say(('<' . join((two201())[1], @a201)) . '>');
say(('<' . join((two201())[1], 1, 2, 3)) . '>');
say(('<' . join((two201())[1], @e201)) . '>');
say(('<' . join((two201())[1], 'only')) . '>');
say(('<' . join((two201())[1], @a201, @a201)) . '>');
say(('<' . join((two201())[1], 0.5, true, false, "", (-7), 3.0)) . '>');
say(('<' . join((two201())[1], two201(), none201(), two201())) . '>');
say(join(','));
say(join(',', ()));
say(join(join('+', 1, 2), 'a', 'b'));
say(join(',', join('-', @a201), join("", @a201)));
say(length(join(',', @a201)));
say(join("", @a201) x 2);
say(join(',', (1 .. 5)) . '!');
say(join(',', @a201[2, 0], (('r') x 3)));
say(join('/', $#a201, scalar(@a201), $a201[1]));
my @a202 = (1, 2, 3);
my @e202;
my @r202;
sub two202() {
    return ('a', 'b');
}
@r202 = (reverse(@a202));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = (reverse(@e202));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = (reverse(7));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = (reverse(@a202, 0, @a202));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = (reverse(reverse(@a202)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = (reverse((1 .. 5)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = (reverse((undef), 1, (undef)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = (reverse(two202(), two202()));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = (0, reverse(@a202), 0);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
say(reverse(@a202));
say(reverse('ab', 'cd'));
say(join(',', reverse(@a202)));
for my $v (reverse(@a202)) {
    say('v', $v);
}
for my $v (reverse((1 .. 3))) {
    push(@a202, $v);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a202) {
        $dump_s .= (defined($a202[$dump_i]) ? (('<' . $a202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a202) . ':') . $dump_s);
}
my ($x202, $y202) = (reverse(1, 2, 3));
say($x202 . $y202);
@a202 = (reverse(@a202));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a202) {
        $dump_s .= (defined($a202[$dump_i]) ? (('<' . $a202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a202) . ':') . $dump_s);
}
push(@r202, reverse(@a202));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
say((reverse(@a202))[0, (-1)]);
say(((reverse(1, 2)) x 2));
