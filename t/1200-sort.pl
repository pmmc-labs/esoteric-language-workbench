# model: t/models/sort.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my @n1 = (10, 9, 2, 33, 100, 1, 21, 2);
my @w1 = ('pear', 'Fig', 'apple', 'fig', "", 'Apple', 'b', 'a10', 'a9');
my @e1;
my @r1;
my @m1 = (3, 1.5, '2', true, false, (-7), 0.25, '10', 1000.0);
@r1 = ((sort @n1));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((sort @w1));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((sort @e1));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((sort @m1));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((sort @n1, @w1));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((sort 7));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((sort 3, 1, 2));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((sort 'b', 'a'));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((sort @n1[0, 1, 2]));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((sort 0, (8 .. 12)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((sort reverse(@n1)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((sort { $a <=> $b } (@n1)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((sort { $a <=> $b } (@e1)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((sort { $a <=> $b } (42)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((sort { $b <=> $a } (@n1)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((sort { $b <=> $a } (@e1)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((sort { $b <=> $a } (42)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((sort { $a cmp $b } (@n1)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((sort { $a cmp $b } (@e1)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((sort { $a cmp $b } (42)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((sort { $b cmp $a } (@n1)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((sort { $b cmp $a } (@e1)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((sort { $b cmp $a } (42)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((sort { $a cmp $b } (@w1)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((sort { $a <=> $b } (@m1)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((sort { $b <=> $a } (@m1)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = (reverse((sort { $a <=> $b } (@n1))));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = (reverse((sort @w1)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
my @w2 = ('pear', 'fig', 'apple', 'kiwi', 'date', 'plum', 'a', 'bb', 'cc', 'ddd', 'ee', 'f');
my @n2 = (5, 3, 8, 1, 9, 2, 7);
my @r2;
sub len2($p) {
    return length($p);
}
sub by2($p, $q) {
    return $p <=> $q;
}
@r2 = ((sort { length($a) <=> length($b) } (@w2)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((sort { (length($a) <=> length($b)) or ($a cmp $b) } (@w2)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((sort { (length($b) <=> length($a)) || ($b cmp $a) } (@w2)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((sort { len2($a) <=> len2($b) } (@w2)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((sort { by2($a, $b) } (@n2)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((sort { $a - $b } (@n2)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((sort { $b - $a } (@n2)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((sort { my $x = $a % 3; my $y = $b % 3; $x <=> $y } (@n2)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((sort { ($a < $b) ? (-1) : (($a > $b) ? 1 : 0) } (@n2)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((sort { scalar(@n2) <=> 0 } (@n2)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((sort { 0 } (@n2)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((sort { 1 } (@n2)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((sort { (-1) } (@n2)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((sort { ($a - $b) / 4 } (@n2)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((sort { ($a - $b) * 0.5 } (@n2)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((sort { $a > $b } (@n2)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((sort { '1' } (@n2)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((sort { true } (@n2)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((sort { false } (@n2)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((sort { 2147483647 } (@n2)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((sort { (-2147483648) } (@n2)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((sort { my @t = ((sort { $b <=> $a } ($a, $b))); $t[0] <=> $a } (@n2)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((sort { (map { $_ % 4 } ($a)) <=> (map { $_ % 4 } ($b)) } (@n2)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((map { my @t = ((sort { $a <=> $b } ($_, 5, 1))); $t[1] } (@n2)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((sort { $b <=> $a } ((map { $_ * $_ } (@n2)))));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((sort { $a <=> $b } ((grep { $_ > 2 } (@n2)))));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((map { $_ + 1 } ((sort { $a <=> $b } (@n2)))));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((grep { length($_) > 2 } ((sort @w2))));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
@r2 = ((sort { ($a + $n2[0]) <=> ($b + $n2[0]) } (@n2)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r2) {
        $dump_s .= (defined($r2[$dump_i]) ? (('<' . $r2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r2) . ':') . $dump_s);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @n2) {
        $dump_s .= (defined($n2[$dump_i]) ? (('<' . $n2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@n2) . ':') . $dump_s);
}
my @n3 = (5, 3, 8, 1);
my @r3;
sub sorted3(@v) {
    return (sort { $a <=> $b } (@v));
}
sub last3(@v) {
    (sort { $b <=> $a } (@v));
}
sub cnt3(@v) {
    return join(',', scalar(@v), @v);
}
sub smallest3(@v) {
    my ($first) = ((sort { $a <=> $b } (@v)));
    return $first;
}
say((sort { $a <=> $b } (@n3)));
say(join(',', (sort { $a <=> $b } (@n3))));
say(cnt3((sort { $a <=> $b } (@n3)), 0));
for my $x ((sort { $a <=> $b } (@n3))) {
    say('x', $x);
}
for ((sort { $a <=> $b } (@n3))) {
    say('i', $_);
}
say($_) for ((sort { $a <=> $b } (@n3)));
my ($x3, $y3) = ((sort { $a <=> $b } (@n3)));
say($x3 . $y3);
say(((sort { $a <=> $b } (@n3)))[0, (-1)]);
say((((sort { $a <=> $b } (@n3))) x 2));
push(@r3, (sort { $a <=> $b } (@n3)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r3) {
        $dump_s .= (defined($r3[$dump_i]) ? (('<' . $r3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r3) . ':') . $dump_s);
}
@r3 = (sorted3(@n3, 4));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r3) {
        $dump_s .= (defined($r3[$dump_i]) ? (('<' . $r3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r3) . ':') . $dump_s);
}
@r3 = (last3(2, 9));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r3) {
        $dump_s .= (defined($r3[$dump_i]) ? (('<' . $r3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r3) . ':') . $dump_s);
}
say(smallest3(@n3));
@n3 = ((sort { $a <=> $b } (@n3)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @n3) {
        $dump_s .= (defined($n3[$dump_i]) ? (('<' . $n3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@n3) . ':') . $dump_s);
}
@n3 = ((sort { $b <=> $a } ((@n3))));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @n3) {
        $dump_s .= (defined($n3[$dump_i]) ? (('<' . $n3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@n3) . ':') . $dump_s);
}
@n3 = (((sort { $a cmp $b } (@n3))));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @n3) {
        $dump_s .= (defined($n3[$dump_i]) ? (('<' . $n3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@n3) . ':') . $dump_s);
}
@n3 = ((sort @n3));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @n3) {
        $dump_s .= (defined($n3[$dump_i]) ? (('<' . $n3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@n3) . ':') . $dump_s);
}
@n3 = (reverse((sort { $a <=> $b } (@n3))));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @n3) {
        $dump_s .= (defined($n3[$dump_i]) ? (('<' . $n3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@n3) . ':') . $dump_s);
}
@n3 = ((sort { $a <=> $b } (@n3, 0)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @n3) {
        $dump_s .= (defined($n3[$dump_i]) ? (('<' . $n3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@n3) . ':') . $dump_s);
}
push(@n3, 6);
$n3[0] = 99;
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @n3) {
        $dump_s .= (defined($n3[$dump_i]) ? (('<' . $n3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@n3) . ':') . $dump_s);
}
@r3 = ((sort { ($a // 0) <=> ($b // 0) } (3, (undef), 1)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r3) {
        $dump_s .= (defined($r3[$dump_i]) ? (('<' . $r3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r3) . ':') . $dump_s);
}
@n3 = (3, (undef), 1);
@r3 = ((sort { ($a // 0) <=> ($b // 0) } (@n3)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r3) {
        $dump_s .= (defined($r3[$dump_i]) ? (('<' . $r3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r3) . ':') . $dump_s);
}
@n3 = (reverse((sort { ($a // 0) <=> ($b // 0) } (@n3))));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @n3) {
        $dump_s .= (defined($n3[$dump_i]) ? (('<' . $n3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@n3) . ':') . $dump_s);
}
