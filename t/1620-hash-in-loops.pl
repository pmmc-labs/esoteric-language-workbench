# model: t/models/hash.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my %h1 = (a => 1, b => 2, c => 3, d => 4);
my $t1 = 0;
for my $v ((sort { $a <=> $b } (values(%h1)))) {
    say($v);
    say($h1{a});
    say(exists($h1{zz}));
    say(scalar(keys(%h1)));
    say(join(',', (sort keys(%h1))));
}
for my $v ((sort %h1)) {
    $t1 = ($t1 . $v);
}
say($t1);
for my $v ($h1{a}, $h1{c}) {
    say($v);
    say($h1{a});
    say(exists($h1{zz}));
    say(scalar(keys(%h1)));
    say(join(',', (sort keys(%h1))));
}
for my $v (@h1{'d', 'a'}) {
    say($v);
    say($h1{a});
    say(exists($h1{zz}));
    say(scalar(keys(%h1)));
    say(join(',', (sort keys(%h1))));
}
for my $v (@h1{('b' . ""), 'b', ('c' . "")}) {
    say($v);
}
for ((sort { $a <=> $b } (values(%h1)))) {
    say($_ * $h1{b});
}
say($_ + $h1{d}) for ((sort { $a <=> $b } (values(%h1))));
say(join(',', (map { $_ + $h1{a} } ((sort { $a <=> $b } (values(%h1)))))));
say(join(',', (grep { exists($h1{$_}) } ((sort %h1)))));
say(join(',', (sort { $b <=> $a } (@h1{'c', 'a', 'd'}))));
say(join(',', (map { $_ . scalar(keys(%h1)) } ($h1{a}, @h1{'b', 'c'}))));
$h1{e} = 5;
delete($h1{a});
say((scalar(keys(%h1)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h1{$_}) ? $h1{$_} : 'undef')) . '>' } ((sort keys(%h1))))));
my %h2 = (a => 1, b => 2, c => 3, d => 4);
for my $k ((sort keys(%h2))) {
    $h2{$k} = ($h2{$k} * 10);
    $h2{$k . 'x'} = 1;
}
say((scalar(keys(%h2)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h2{$_}) ? $h2{$_} : 'undef')) . '>' } ((sort keys(%h2))))));
for my $k ((sort keys(%h2))) {
    if ($k eq 'b') {
        delete($h2{$k});
    }
}
say((scalar(keys(%h2)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h2{$_}) ? $h2{$_} : 'undef')) . '>' } ((sort keys(%h2))))));
say(join(',', (map { $h2{$_} = 0; $_ } ((sort keys(%h2))))));
say((scalar(keys(%h2)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h2{$_}) ? $h2{$_} : 'undef')) . '>' } ((sort keys(%h2))))));
say(join(',', (grep { delete($h2{$_}) } ((sort keys(%h2))))));
say((scalar(keys(%h2)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h2{$_}) ? $h2{$_} : 'undef')) . '>' } ((sort keys(%h2))))));
for my $i ((1 .. scalar(keys(%h2)))) {
    $h2{'n' . $i} = $i;
}
say((scalar(keys(%h2)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h2{$_}) ? $h2{$_} : 'undef')) . '>' } ((sort keys(%h2))))));
my %h3 = (a => 1, b => 2, c => 3, d => 4);
my %o3 = (a => 1, b => 2, c => 3, d => 4);
for my $v ((sort { $a <=> $b } (values(%h3)))) {
    last;
}
$h3{a} = 10;
for my $v ((sort { $a <=> $b } (values(%h3)))) {
    next;
    say('not reached');
}
$h3{b} = 20;
OUT: for my $v ((sort { $a <=> $b } (values(%h3)))) {
    for my $w ((sort { $a <=> $b } (values(%o3)))) {
        last OUT;
    }
}
$h3{c} = 30;
$o3{c} = 30;
for my $v ((sort { $a <=> $b } (@h3{'a', 'b'}))) {
    for my $w ((sort { $a <=> $b } (values(%h3)))) {
        say($v . $w);
    }
}
$h3{d} = 40;
sub first3() {
    for my $v ((sort { $a <=> $b } (values(%h3)))) {
        return $v;
    }
    return 0;
}
say(first3());
$h3{e} = 50;
sub n3($x) {
    return $x + scalar(keys(%h3));
}
say(join(',', (map { n3($_) } ((sort { $a <=> $b } (values(%o3)))))));
$o3{e} = 5;
say((scalar(keys(%h3)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h3{$_}) ? $h3{$_} : 'undef')) . '>' } ((sort keys(%h3))))));
say((scalar(keys(%o3)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($o3{$_}) ? $o3{$_} : 'undef')) . '>' } ((sort keys(%o3))))));
sub own3() {
    my %t = (p => 1, q => 2);
    for my $v ((sort { $a <=> $b } (values(%t)))) {
        if ($v == 2) {
            return scalar(keys(%t));
        }
    }
    return 0;
}
say(own3());
say(own3());
