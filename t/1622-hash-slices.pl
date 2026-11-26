# model: t/models/hash.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my %h1 = (a => 1, b => 2, c => 3, d => 4);
my $k1 = 'b';
my @a1 = ('c', 'a');
my @l1;
@l1 = (@h1{'a', 'b'});
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @l1) {
        $dump_s .= (defined($l1[$dump_i]) ? (('<' . $l1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@l1) . ':') . $dump_s);
}
@l1 = (@h1{'d', 'nope', 'a'});
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @l1) {
        $dump_s .= (defined($l1[$dump_i]) ? (('<' . $l1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@l1) . ':') . $dump_s);
}
@l1 = (@h1{$k1, ($k1 . 'x'), ('c' . "")});
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @l1) {
        $dump_s .= (defined($l1[$dump_i]) ? (('<' . $l1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@l1) . ':') . $dump_s);
}
@l1 = (@h1{@a1});
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @l1) {
        $dump_s .= (defined($l1[$dump_i]) ? (('<' . $l1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@l1) . ':') . $dump_s);
}
@l1 = (@h1{@a1, 'd'});
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @l1) {
        $dump_s .= (defined($l1[$dump_i]) ? (('<' . $l1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@l1) . ':') . $dump_s);
}
@l1 = (@h1{(sort keys(%h1))});
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @l1) {
        $dump_s .= (defined($l1[$dump_i]) ? (('<' . $l1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@l1) . ':') . $dump_s);
}
@l1 = (@h1{'a', 'a'});
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @l1) {
        $dump_s .= (defined($l1[$dump_i]) ? (('<' . $l1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@l1) . ':') . $dump_s);
}
@l1 = (@h1{1, 2});
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @l1) {
        $dump_s .= (defined($l1[$dump_i]) ? (('<' . $l1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@l1) . ':') . $dump_s);
}
say((scalar(keys(%h1)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h1{$_}) ? $h1{$_} : 'undef')) . '>' } ((sort keys(%h1))))));
my @v1 = (@h1{'b', 'c'});
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @v1) {
        $dump_s .= (defined($v1[$dump_i]) ? (('<' . $v1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@v1) . ':') . $dump_s);
}
my @w1 = (@h1{'a', 'b'}, 9, @h1{'c', 'd'});
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @w1) {
        $dump_s .= (defined($w1[$dump_i]) ? (('<' . $w1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@w1) . ':') . $dump_s);
}
my ($p1, $q1) = (@h1{'c', 'd'});
say($p1 + $q1);
say(scalar(@v1));
say(join('-', reverse(@h1{'a', 'b', 'c'})));
sub cnt1(@r) {
    return scalar(@r);
}
say(cnt1(@h1{'a', 'b', 'c'}));
say(cnt1(0, @h1{'d', 'a'}));
my %o1 = (x => 0, @h1{'a', 'b'});
say((scalar(keys(%o1)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($o1{$_}) ? $o1{$_} : 'undef')) . '>' } ((sort keys(%o1))))));
say(scalar(@w1));
my %h2 = (a => 1, b => 2, c => 3, d => 4);
my @a2 = (1, 2, 3);
my $i2 = 0;
@h2{'a', 'b'} = (10, 20);
say((scalar(keys(%h2)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h2{$_}) ? $h2{$_} : 'undef')) . '>' } ((sort keys(%h2))))));
@h2{'x', 'y'} = (1, 2);
say((scalar(keys(%h2)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h2{$_}) ? $h2{$_} : 'undef')) . '>' } ((sort keys(%h2))))));
@h2{'c', 'new', 'more'} = (30);
say((scalar(keys(%h2)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h2{$_}) ? $h2{$_} : 'undef')) . '>' } ((sort keys(%h2))))));
@h2{'p', 'q'} = ();
say((scalar(keys(%h2)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h2{$_}) ? $h2{$_} : 'undef')) . '>' } ((sort keys(%h2))))));
@h2{'a', 'b'} = (1, 2, 3, 4);
say((scalar(keys(%h2)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h2{$_}) ? $h2{$_} : 'undef')) . '>' } ((sort keys(%h2))))));
@h2{'a', 'b'} = (@h2{'b', 'a'});
say((scalar(keys(%h2)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h2{$_}) ? $h2{$_} : 'undef')) . '>' } ((sort keys(%h2))))));
@h2{'k', 'k'} = (1, 2);
say((scalar(keys(%h2)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h2{$_}) ? $h2{$_} : 'undef')) . '>' } ((sort keys(%h2))))));
@h2{@a2, 'z'} = (@a2, 26);
say((scalar(keys(%h2)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h2{$_}) ? $h2{$_} : 'undef')) . '>' } ((sort keys(%h2))))));
my $n2 = 'one';
@h2{$n2, ($n2 . '!')} = (($n2 = 'two'), 2);
say((scalar(keys(%h2)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h2{$_}) ? $h2{$_} : 'undef')) . '>' } ((sort keys(%h2))))));
@a2[0, 1] = ('x', 'y');
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a2) {
        $dump_s .= (defined($a2[$dump_i]) ? (('<' . $a2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a2) . ':') . $dump_s);
}
@a2[2, 4] = ('z');
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a2) {
        $dump_s .= (defined($a2[$dump_i]) ? (('<' . $a2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a2) . ':') . $dump_s);
}
@a2[(-1), 0] = (9, 8);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a2) {
        $dump_s .= (defined($a2[$dump_i]) ? (('<' . $a2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a2) . ':') . $dump_s);
}
@a2[(1 .. 3)] = (1, 2, 3);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a2) {
        $dump_s .= (defined($a2[$dump_i]) ? (('<' . $a2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a2) . ':') . $dump_s);
}
@a2[1, 1] = (5, 6);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a2) {
        $dump_s .= (defined($a2[$dump_i]) ? (('<' . $a2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a2) . ':') . $dump_s);
}
@a2[0, 1] = (@a2[1, 0]);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a2) {
        $dump_s .= (defined($a2[$dump_i]) ? (('<' . $a2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a2) . ':') . $dump_s);
}
@a2[6, 5] = ();
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a2) {
        $dump_s .= (defined($a2[$dump_i]) ? (('<' . $a2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a2) . ':') . $dump_s);
}
@a2[$i2, ($i2 + 1)] = (($i2 = 3), 7);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a2) {
        $dump_s .= (defined($a2[$dump_i]) ? (('<' . $a2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a2) . ':') . $dump_s);
}
my %h3 = (a => 1, b => 2, c => 3, d => 4);
my @l3;
@l3 = (delete(@h3{'a', 'c'}));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @l3) {
        $dump_s .= (defined($l3[$dump_i]) ? (('<' . $l3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@l3) . ':') . $dump_s);
}
say((scalar(keys(%h3)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h3{$_}) ? $h3{$_} : 'undef')) . '>' } ((sort keys(%h3))))));
@l3 = (delete(@h3{'a', 'b', 'nope'}));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @l3) {
        $dump_s .= (defined($l3[$dump_i]) ? (('<' . $l3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@l3) . ':') . $dump_s);
}
say((scalar(keys(%h3)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h3{$_}) ? $h3{$_} : 'undef')) . '>' } ((sort keys(%h3))))));
@l3 = (delete(@h3{'d', 'd'}));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @l3) {
        $dump_s .= (defined($l3[$dump_i]) ? (('<' . $l3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@l3) . ':') . $dump_s);
}
say((scalar(keys(%h3)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h3{$_}) ? $h3{$_} : 'undef')) . '>' } ((sort keys(%h3))))));
my %o3 = (a => 1, b => 2, c => 3, d => 4);
my @got3 = (delete(@o3{(sort keys(%o3))}));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @got3) {
        $dump_s .= (defined($got3[$dump_i]) ? (('<' . $got3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@got3) . ':') . $dump_s);
}
say((scalar(keys(%o3)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($o3{$_}) ? $o3{$_} : 'undef')) . '>' } ((sort keys(%o3))))));
