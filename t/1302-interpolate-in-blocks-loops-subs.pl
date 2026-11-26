# model: t/models/interp.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my @a1 = (3, 'b', 1.5, true, "");
my @r1;
my $n1 = 0;
for (@a1) {
    say("<$_>");
}
say("$_:") for (@a1);
say("${_}_") for (1, 2);
for my $v (@a1) {
    say("$v/@a1");
}
@r1 = ((map { "$_-" } (@a1)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((map { ("a$_", "$_") } (@a1)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((grep { "$_" ne "" } (@a1)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((grep { "$_" } (@a1)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((sort { "$a" cmp "$b" } (@a1)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((sort { "${b}!" cmp "${a}!" } (@a1)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((sort 'z', "@a1", "$a1[1]", "a${n1}"));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((map { "$_.$n1 of $#a1" } (1, 2, 3)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
@r1 = ((map { "$a1[$_]|@a1[$_, 0 .. $_]" } (0, 1)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @r1) {
        $dump_s .= (defined($r1[$dump_i]) ? (('<' . $r1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@r1) . ':') . $dump_s);
}
my @a2 = (1, 2);
my $x2 = 3;
for my $v ("@a2") {
    push(@a2, 3);
    say($v);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a2) {
        $dump_s .= (defined($a2[$dump_i]) ? (('<' . $a2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a2) . ':') . $dump_s);
}
for my $v ("$a2[0]", "@a2[0, 1]", "$#a2") {
    $a2[0] = 9;
    push(@a2, 4);
    say($v);
}
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a2) {
        $dump_s .= (defined($a2[$dump_i]) ? (('<' . $a2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a2) . ':') . $dump_s);
}
for my $v ("$x2", "$x2-") {
    $x2 = 5;
    say($v);
}
say($x2);
@a2 = (1, 2);
@a2 = ((map { "$_!" } ("@a2", "$a2[1]")));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a2) {
        $dump_s .= (defined($a2[$dump_i]) ? (('<' . $a2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a2) . ':') . $dump_s);
}
my $k2 = 0;
while ($k2 < 2) {
    say("k=$k2 $a2[$k2]");
    $k2++;
}
say("yes $x2") if "$x2" eq '5';
if ("$x2") {
    say("true: $x2");
}
my @a3 = ('p', 'q');
sub show3($s, $t) {
    return "[$s|$t]";
}
sub all3() {
    return "@a3";
}
sub lastly3() {
    "@a3!";
}
say(show3("@a3", "$a3[0]$#a3"));
my $v3 = all3();
say($v3);
my $w3 = lastly3();
say($w3);
say(all3(), lastly3());
say(join("-$#a3-", "@a3", "$a3[1]"));
say("@a3", "@a3");
say(reverse("a$a3[0]", "b$a3[1]"));
