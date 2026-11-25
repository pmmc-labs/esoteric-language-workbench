# model: t/models/it.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my @a101 = (1, 2, 3);
my @e101;
my @r101;
sub two101() {
    return ('p', 'q');
}
sub twice101($p) {
    return $p * 2;
}
@r101 = ((map { $_ * 2 } (@a101)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { ($_, ($_ + 10)) } (@a101)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { () } (@a101)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { ($_ > 1) ? ($_) : () } (@a101)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { twice101($_) } (@a101)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { (two101(), $_) } (@a101)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { @a101 } (@a101)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { ($_) x 2 } (@a101)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { 1 .. $_ } (@a101)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { reverse($_, 0) } (@a101)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { (undef) } (@a101)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { ('<' . $_) . '>' } (@a101)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { ($_ == 2) ? 'two' : $_ } (@a101)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { my $t = $_ * $_; $t + 1 } (@a101)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { my $t = $_; $t *= 3; $t = 0 if $_ == 2; $t } (@a101)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { my @m; push(@m, $_, $_); @m } (@a101)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { scalar(@a101) } (@a101)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { $a101[$_ - 1] } (@a101)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { join('-', $_, $_) } (@a101)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { defined($_) ? (('<' . $_) . '>') : 'undef' } (1, 2, 3)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { defined($_) ? (('<' . $_) . '>') : 'undef' } (@e101)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { defined($_) ? (('<' . $_) . '>') : 'undef' } (())));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { defined($_) ? (('<' . $_) . '>') : 'undef' } (@a101, 9, @e101)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { defined($_) ? (('<' . $_) . '>') : 'undef' } (@a101[2, 0])));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { defined($_) ? (('<' . $_) . '>') : 'undef' } ((2 .. 4))));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { defined($_) ? (('<' . $_) . '>') : 'undef' } (((@a101) x 2))));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { defined($_) ? (('<' . $_) . '>') : 'undef' } ($a101[0], $a101[2])));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { defined($_) ? (('<' . $_) . '>') : 'undef' } (two101())));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { defined($_) ? (('<' . $_) . '>') : 'undef' } (reverse(@a101))));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { defined($_) ? (('<' . $_) . '>') : 'undef' } ((0 ? @a101 : @e101))));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { defined($_) ? (('<' . $_) . '>') : 'undef' } ((undef), 0, "")));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { defined($_) ? (('<' . $_) . '>') : 'undef' } ((map { $_ * 3 } (@a101)))));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
@r101 = ((map { defined($_) ? (('<' . $_) . '>') : 'undef' } ((grep { $_ > 1 } (@a101)))));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r101) {
        $dump_s .= (defined($r101[$dump_i]) ? (('<' . $r101[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r101) . ':') . $dump_s);
}
my @a102 = (1, 2, 3);
my @r102;
sub cnt102(@v) {
    return join(',', scalar(@v), @v);
}
sub mapped102(@v) {
    return (map { $_ + 100 } (@v));
}
sub last102(@v) {
    (map { -$_ } (@v));
}
say((map { $_ * 2 } (@a102)));
say('[', (map { $_ * 2 } (@a102)), '|', (map { ($_, $_) } (@a102)), ']');
say(join(',', (map { $_ * 2 } (@a102))));
say(cnt102((map { $_ * 2 } (@a102))));
say(cnt102(0, (map { ($_, $_) } (@a102)), 0));
my ($x102, $y102) = ((map { $_ * 2 } (@a102)));
say($x102 . $y102);
push(@r102, (map { $_ * 2 } (@a102)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r102) {
        $dump_s .= (defined($r102[$dump_i]) ? (('<' . $r102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r102) . ':') . $dump_s);
}
for my $v ((map { $_ * 2 } (@a102))) {
    say('v', $v);
}
for ((map { ($_, $_) } (@a102))) {
    say('i', $_);
}
say(((map { $_ * 2 } (@a102)))[2, 0]);
say(reverse((map { $_ * 2 } (@a102))));
say((((map { $_ * 2 } (@a102))) x 2));
say($_) for ((map { $_ * 2 } (@a102)));
@r102 = (mapped102(@a102));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r102) {
        $dump_s .= (defined($r102[$dump_i]) ? (('<' . $r102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r102) . ':') . $dump_s);
}
@r102 = (last102(5, 6));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r102) {
        $dump_s .= (defined($r102[$dump_i]) ? (('<' . $r102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r102) . ':') . $dump_s);
}
@a102 = ((map { $_ * 10 } (@a102)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a102) {
        $dump_s .= (defined($a102[$dump_i]) ? (('<' . $a102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a102) . ':') . $dump_s);
}
@a102 = ((map { ($_, $_) } (@a102)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a102) {
        $dump_s .= (defined($a102[$dump_i]) ? (('<' . $a102[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a102) . ':') . $dump_s);
}
my $n102 = (map { ($_, $_) } (@a102));
say($n102);
say((map { $_ * 2 } (@a102)) + 1);
say('n' . (map { $_ * 2 } (@a102)));
say(scalar(@a102));
if ((map { () } (@a102))) {
    say('never');
} elsif ((map { $_ * 2 } (@a102))) {
    say('some');
}
say((map { $_ } (())) ? 'yes' : 'no');
say($a102[(map { $_ } (1, 2))]);
(map { push(@r102, $_); 0 } (@a102));
say(scalar(@r102));
my @a103 = (1, 2, 3);
my @r103;
sub row103($p) {
    return join("", (map { $_ * $p } ((1 .. $p))));
}
@r103 = ((map { my $o = $_; (map { $o . $_ } ((1 .. $o))) } (@a103)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r103) {
        $dump_s .= (defined($r103[$dump_i]) ? (('<' . $r103[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r103) . ':') . $dump_s);
}
@r103 = ((map { (map { $_ * 2 } ($_, ($_ + 10))) } (@a103)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r103) {
        $dump_s .= (defined($r103[$dump_i]) ? (('<' . $r103[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r103) . ':') . $dump_s);
}
@r103 = ((map { $_ + 1 } ((map { ($_, $_) } (@a103)))));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r103) {
        $dump_s .= (defined($r103[$dump_i]) ? (('<' . $r103[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r103) . ':') . $dump_s);
}
@r103 = ((map { row103($_) } (@a103)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r103) {
        $dump_s .= (defined($r103[$dump_i]) ? (('<' . $r103[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r103) . ':') . $dump_s);
}
@r103 = ((map { my $t = 0; $t += $_ for ((1 .. $_)); ($_ . ':') . $t } (@a103)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r103) {
        $dump_s .= (defined($r103[$dump_i]) ? (('<' . $r103[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r103) . ':') . $dump_s);
}
@r103 = ((map { my $t = ""; for (@a103) { $t .= $_; } $_ . $t } (@a103)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r103) {
        $dump_s .= (defined($r103[$dump_i]) ? (('<' . $r103[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r103) . ':') . $dump_s);
}
for (@a103) {
    say($_, ':', (map { $_ * $_ } ((1 .. $_))), ':', $_);
}
@r103 = ((map { join('+', (map { $_ } (@a103))) } (@a103)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r103) {
        $dump_s .= (defined($r103[$dump_i]) ? (('<' . $r103[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r103) . ':') . $dump_s);
}
@r103 = ((map { $_ + $a103[0] } (@a103)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r103) {
        $dump_s .= (defined($r103[$dump_i]) ? (('<' . $r103[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r103) . ':') . $dump_s);
}
@r103 = ((map { scalar(@a103) } (@a103)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r103) {
        $dump_s .= (defined($r103[$dump_i]) ? (('<' . $r103[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r103) . ':') . $dump_s);
}
