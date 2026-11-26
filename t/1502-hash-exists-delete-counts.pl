# model: t/models/hash.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my %h1 = (a => 1, u => (undef), z => 0, e => "", 1, 'one');
my $k1 = 'a';
say(exists($h1{a}));
say(exists($h1{u}));
say(exists($h1{nope}));
say(exists($h1{$k1}));
say(exists($h1{1}));
say(exists($h1{$k1 . 'x'}));
say(!exists($h1{nope}));
say(exists($h1{z}) ? 'has z' : 'no z');
say(exists($h1{a}) && exists($h1{e}));
if (exists($h1{nope})) {
    say('wrong');
} elsif (exists($h1{u})) {
    say('u is there');
}
say((scalar(keys(%h1)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h1{$_}) ? $h1{$_} : 'undef')) . '>' } ((sort keys(%h1))))));
say(delete($h1{a}) // 'undef');
say(delete($h1{a}) // 'undef');
say(delete($h1{u}) // 'undef');
say(delete($h1{nope}) // 'undef');
say(exists($h1{a}));
say((scalar(keys(%h1)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h1{$_}) ? $h1{$_} : 'undef')) . '>' } ((sort keys(%h1))))));
my $d1 = delete($h1{1});
say($d1);
delete($h1{z});
say((scalar(keys(%h1)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h1{$_}) ? $h1{$_} : 'undef')) . '>' } ((sort keys(%h1))))));
$h1{a} = 'back';
say(length(delete($h1{a})) + 1);
say((scalar(keys(%h1)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h1{$_}) ? $h1{$_} : 'undef')) . '>' } ((sort keys(%h1))))));
delete($h1{e});
say((scalar(keys(%h1)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h1{$_}) ? $h1{$_} : 'undef')) . '>' } ((sort keys(%h1))))));
say(delete($h1{e}) // 'undef');
my %h2 = (a => 1, b => 2, c => 3, d => 4);
my %e2;
say(keys(%h2) + 0);
my $n2 = %h2;
say($n2);
my $m2 = keys(%h2);
say($m2);
my $z2 = %e2;
say($z2);
if (%h2) {
    say('some');
} else {
    say('none');
}
if (%e2) {
    say('some');
} else {
    say('none');
}
if (keys(%e2)) {
    say('keys');
} else {
    say('no keys');
}
if (values(%h2)) {
    say('values');
}
say(keys(%h2) + values(%h2));
say(keys(%h2) == 4);
say('n' . keys(%h2));
delete($h2{a});
my $after2 = %h2;
say($after2);
$h2{a} = 9;
$h2{a} = 10;
my $again2 = %h2;
say($again2);
say(join(',', (sort keys(%h2))));
say(join(',', (sort { $a <=> $b } (values(%h2)))));
say(join(',', (sort %h2)));
say(join(',', reverse((sort keys(%h2)))));
say(join(',', (map { $_ x 2 } ((sort keys(%h2))))));
my %h3 = (a => 1, b => 2, c => 3, d => 4);
my %o3 = (%h3);
$o3{a} = 9;
$o3{z} = 0;
delete($o3{b});
say((scalar(keys(%h3)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h3{$_}) ? $h3{$_} : 'undef')) . '>' } ((sort keys(%h3))))));
say((scalar(keys(%o3)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($o3{$_}) ? $o3{$_} : 'undef')) . '>' } ((sort keys(%o3))))));
%o3 = (%h3);
say((scalar(keys(%o3)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($o3{$_}) ? $o3{$_} : 'undef')) . '>' } ((sort keys(%o3))))));
%h3 = (%h3);
say((scalar(keys(%h3)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h3{$_}) ? $h3{$_} : 'undef')) . '>' } ((sort keys(%h3))))));
%h3 = (%h3, e => 5);
say((scalar(keys(%h3)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h3{$_}) ? $h3{$_} : 'undef')) . '>' } ((sort keys(%h3))))));
%h3 = (first => 0, %h3);
say((scalar(keys(%h3)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h3{$_}) ? $h3{$_} : 'undef')) . '>' } ((sort keys(%h3))))));
my @a3 = ((sort %h3));
say(scalar(@a3));
my @k3 = ((sort keys(%h3)));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @k3) {
        $dump_s .= (defined($k3[$dump_i]) ? (('<' . $k3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@k3) . ':') . $dump_s);
}
my @v3 = ((sort { $a <=> $b } (values(%h3))));
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @v3) {
        $dump_s .= (defined($v3[$dump_i]) ? (('<' . $v3[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@v3) . ':') . $dump_s);
}
sub size3($n) {
    return $n * 2;
}
say(size3((keys(%h3) + 0)));
say(size3((%h3 + 0)));
sub made3() {
    my %t = (p => 1, q => 2);
    return %t;
}
my %r3 = (made3());
say((scalar(keys(%r3)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($r3{$_}) ? $r3{$_} : 'undef')) . '>' } ((sort keys(%r3))))));
sub twice3() {
    my %t = (p => 1);
    $t{q} = 2;
    return keys(%t);
}
my @tw3 = (twice3());
say(join(',', (sort @tw3)));
{
    my %t = (in => 1);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
    {
        my %t = (deeper => 2);
        say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
    }
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
my $i3 = 0;
while ($i3 < 3) {
    my %t = (k => $i3);
    $t{'x' . $i3} = 1;
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
    $i3++;
}
