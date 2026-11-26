# kind: new
# D27: a hash keeps its keys in the order they were first stored. perl's order is its own, so perl is not asked.
# model: t/models/hash.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my %h1 = (one => 1, two => 2, three => 3, four => 4);
say((((join(',', keys(%h1)) . '|') . join(',', values(%h1))) . '|') . join(',', %h1));
$h1{five} = 5;
$h1{two} = 22;
say((((join(',', keys(%h1)) . '|') . join(',', values(%h1))) . '|') . join(',', %h1));
$h1{three} += 1;
$h1{one}++;
$h1{six} //= 6;
$h1{four} &&= 0;
say((((join(',', keys(%h1)) . '|') . join(',', values(%h1))) . '|') . join(',', %h1));
delete($h1{one});
say((((join(',', keys(%h1)) . '|') . join(',', values(%h1))) . '|') . join(',', %h1));
$h1{one} = 11;
say((((join(',', keys(%h1)) . '|') . join(',', values(%h1))) . '|') . join(',', %h1));
delete($h1{six});
delete($h1{two});
$h1{two} = 2;
$h1{six} = 6;
say((((join(',', keys(%h1)) . '|') . join(',', values(%h1))) . '|') . join(',', %h1));
my %o1 = (a => 1, b => 2, a => 3, c => 4, b => 5, d => 6);
say((((join(',', keys(%o1)) . '|') . join(',', values(%o1))) . '|') . join(',', %o1));
%o1 = (z => 0, %h1, last => 9, two => 'again');
say((((join(',', keys(%o1)) . '|') . join(',', values(%o1))) . '|') . join(',', %o1));
%o1 = (%o1, z => 1);
say((((join(',', keys(%o1)) . '|') . join(',', values(%o1))) . '|') . join(',', %o1));
%h1 = (%h1);
say((((join(',', keys(%h1)) . '|') . join(',', values(%h1))) . '|') . join(',', %h1));
%h1 = ();
say((((join(',', keys(%h1)) . '|') . join(',', values(%h1))) . '|') . join(',', %h1));
%h1 = (10, 'a', 9, 'b', 100, 'c', 1, 'd', 9.0, 'e');
say((((join(',', keys(%h1)) . '|') . join(',', values(%h1))) . '|') . join(',', %h1));
say(defined($h1{nope}));
say(exists($h1{none}));
$h1{nope} = 1;
say((((join(',', keys(%h1)) . '|') . join(',', values(%h1))) . '|') . join(',', %h1));
my %h2;
my $i2 = 0;
while ($i2 < 40) {
    $h2{'k' . $i2} = $i2;
    $i2++;
}
say((((join(',', keys(%h2)) . '|') . join(',', values(%h2))) . '|') . join(',', %h2));
$i2 = 0;
while ($i2 < 40) {
    if (($i2 != 3) && (($i2 != 17) && ($i2 != 31))) {
        delete($h2{'k' . $i2});
    }
    $i2++;
}
say((((join(',', keys(%h2)) . '|') . join(',', values(%h2))) . '|') . join(',', %h2));
$h2{k5} = 5;
$h2{k10} = 'ten';
$h2{k4} = 4;
say((((join(',', keys(%h2)) . '|') . join(',', values(%h2))) . '|') . join(',', %h2));
$i2 = 0;
while ($i2 < 12) {
    $h2{'n' . $i2} = $i2;
    delete($h2{'n' . ($i2 - 1)});
    $i2++;
}
say((((join(',', keys(%h2)) . '|') . join(',', values(%h2))) . '|') . join(',', %h2));
my @a2 = (keys(%h2));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @a2) {
        $dump_s .= (defined($a2[$dump_i]) ? (('<' . $a2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@a2) . ':') . $dump_s);
}
my @v2 = (values(%h2));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @v2) {
        $dump_s .= (defined($v2[$dump_i]) ? (('<' . $v2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@v2) . ':') . $dump_s);
}
my @p2 = (%h2);
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @p2) {
        $dump_s .= (defined($p2[$dump_i]) ? (('<' . $p2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@p2) . ':') . $dump_s);
}
sub made2() {
    my %t = (y => 1, x => 2, w => 3);
    $t{a} = 0;
    return %t;
}
my %r2 = (made2());
say((((join(',', keys(%r2)) . '|') . join(',', values(%r2))) . '|') . join(',', %r2));
my @l2 = (made2(), keys(%r2));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @l2) {
        $dump_s .= (defined($l2[$dump_i]) ? (('<' . $l2[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@l2) . ':') . $dump_s);
}
