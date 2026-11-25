# model: t/models/it.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my @a201 = (1, 2, 3, 4, 5, 6);
my @v201;
my @r201;
sub odd201($p) {
    return $p % 2;
}
push(@v201, 0);
push(@v201, 1);
push(@v201, (-7));
push(@v201, 0.5);
push(@v201, 3.0);
push(@v201, "");
push(@v201, '0');
push(@v201, 'ab');
push(@v201, '00');
push(@v201, ' 3 ');
push(@v201, true);
push(@v201, false);
push(@v201, (undef));
@r201 = ((grep { $_ } (@v201)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r201) {
        $dump_s .= (defined($r201[$dump_i]) ? (('<' . $r201[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r201) . ':') . $dump_s);
}
@r201 = ((grep { !$_ } (@v201)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r201) {
        $dump_s .= (defined($r201[$dump_i]) ? (('<' . $r201[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r201) . ':') . $dump_s);
}
@r201 = ((grep { defined($_) } (@v201)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r201) {
        $dump_s .= (defined($r201[$dump_i]) ? (('<' . $r201[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r201) . ':') . $dump_s);
}
@r201 = ((grep { $_ // 1 } (@v201)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r201) {
        $dump_s .= (defined($r201[$dump_i]) ? (('<' . $r201[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r201) . ':') . $dump_s);
}
@r201 = ((grep { 1 } (@v201)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r201) {
        $dump_s .= (defined($r201[$dump_i]) ? (('<' . $r201[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r201) . ':') . $dump_s);
}
@r201 = ((grep { 0 } (@v201)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r201) {
        $dump_s .= (defined($r201[$dump_i]) ? (('<' . $r201[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r201) . ':') . $dump_s);
}
@r201 = ((grep { "" } (@v201)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r201) {
        $dump_s .= (defined($r201[$dump_i]) ? (('<' . $r201[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r201) . ':') . $dump_s);
}
@r201 = ((grep { '0' } (@v201)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r201) {
        $dump_s .= (defined($r201[$dump_i]) ? (('<' . $r201[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r201) . ':') . $dump_s);
}
@r201 = ((grep { '00' } (@v201)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r201) {
        $dump_s .= (defined($r201[$dump_i]) ? (('<' . $r201[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r201) . ':') . $dump_s);
}
@r201 = ((grep { (undef) } (@v201)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r201) {
        $dump_s .= (defined($r201[$dump_i]) ? (('<' . $r201[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r201) . ':') . $dump_s);
}
@r201 = ((grep { defined($_) && ($_ ne "") } (@v201)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r201) {
        $dump_s .= (defined($r201[$dump_i]) ? (('<' . $r201[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r201) . ':') . $dump_s);
}
@r201 = ((grep { $_ > 2 } (@a201)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r201) {
        $dump_s .= (defined($r201[$dump_i]) ? (('<' . $r201[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r201) . ':') . $dump_s);
}
@r201 = ((grep { $_ % 2 } (@a201)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r201) {
        $dump_s .= (defined($r201[$dump_i]) ? (('<' . $r201[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r201) . ':') . $dump_s);
}
@r201 = ((grep { odd201($_) } (@a201)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r201) {
        $dump_s .= (defined($r201[$dump_i]) ? (('<' . $r201[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r201) . ':') . $dump_s);
}
@r201 = ((grep { $_ == $a201[2] } (@a201)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r201) {
        $dump_s .= (defined($r201[$dump_i]) ? (('<' . $r201[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r201) . ':') . $dump_s);
}
@r201 = ((grep { my $h = $_ * 2; $h > 7 } (@a201)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r201) {
        $dump_s .= (defined($r201[$dump_i]) ? (('<' . $r201[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r201) . ':') . $dump_s);
}
@r201 = ((grep { ($_ > 1) && ($_ < 5) } (@a201)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r201) {
        $dump_s .= (defined($r201[$dump_i]) ? (('<' . $r201[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r201) . ':') . $dump_s);
}
@r201 = ((grep { scalar(@a201) } (@a201)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r201) {
        $dump_s .= (defined($r201[$dump_i]) ? (('<' . $r201[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r201) . ':') . $dump_s);
}
@r201 = ((grep { ($_ == 3) ? 0 : 1 } (@a201)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r201) {
        $dump_s .= (defined($r201[$dump_i]) ? (('<' . $r201[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r201) . ':') . $dump_s);
}
@r201 = ((grep { (grep { $_ > 5 } (@a201)) } (@a201)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r201) {
        $dump_s .= (defined($r201[$dump_i]) ? (('<' . $r201[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r201) . ':') . $dump_s);
}
@r201 = ((grep { (map { $_ } (())) } (@a201)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r201) {
        $dump_s .= (defined($r201[$dump_i]) ? (('<' . $r201[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r201) . ':') . $dump_s);
}
my @a202 = (1, 2, 3, 4);
my @e202;
my @r202;
sub cnt202(@v) {
    return join(',', scalar(@v), @v);
}
sub has202($p) {
    return (grep { $_ == $p } (@a202)) ? 'yes' : 'no';
}
sub kept202(@v) {
    return (grep { $_ < 3 } (@v));
}
say((grep { $_ > 2 } (@a202)));
say(join(',', (grep { $_ > 2 } (@a202))));
say(cnt202((grep { $_ > 2 } (@a202)), 9));
for my $x ((grep { $_ > 2 } (@a202))) {
    say('x', $x);
}
say($_) for ((grep { $_ > 2 } (@a202)));
my ($x202, $y202) = ((grep { $_ > 2 } (@a202)));
say($x202 . $y202);
@r202 = (reverse((grep { $_ > 2 } (@a202))));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = ((map { $_ * 2 } ((grep { $_ > 2 } (@a202)))));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = ((grep { $_ > 4 } ((map { $_ * 2 } (@a202)))));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = ((grep { 1 } (@e202)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = ((grep { 1 } (())));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = ((grep { $_ > 3 } (@a202, 9, @a202)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = ((grep { ($_ % 3) == 0 } ((1 .. 10))));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = ((grep { 1 } (@a202[3, 0])));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@r202 = (kept202(@a202, 0));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
my $n202 = (grep { $_ > 2 } (@a202));
say($n202);
say((grep { $_ > 2 } (@a202)) + 0);
say('n' . (grep { 0 } (@a202)));
if ((grep { $_ == 9 } (@a202))) {
    say('never');
} elsif ((grep { $_ == 2 } (@a202))) {
    say('has 2');
}
say(has202(3));
say(has202(7));
while ((grep { $_ > 2 } (@a202)) > 0) {
    pop(@a202);
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
@a202 = (5, 6, 7);
@r202 = ((grep { 1 } (@a202)));
$r202[0] = 'r';
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a202) {
        $dump_s .= (defined($a202[$dump_i]) ? (('<' . $a202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a202) . ':') . $dump_s);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
@a202 = ((grep { $_ > 5 } (@a202)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a202) {
        $dump_s .= (defined($a202[$dump_i]) ? (('<' . $a202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a202) . ':') . $dump_s);
}
(grep { push(@r202, $_); 1 } (@a202));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r202) {
        $dump_s .= (defined($r202[$dump_i]) ? (('<' . $r202[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r202) . ':') . $dump_s);
}
