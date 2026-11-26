# model: t/models/hash.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my %h1 = ('k0', 0, 'k1', 1, 'k2', (-7), 'k3', 0.5, 'k4', 3.0, 'k5', "", 'k6', '0', 'k7', 'ab', 'k8', '00', 'k9', ' 3 ', 'k10', true, 'k11', false, 'k12', (undef));
say((scalar(keys(%h1)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h1{$_}) ? $h1{$_} : 'undef')) . '>' } ((sort keys(%h1))))));
say(defined($h1{k0}) ? (('[' . $h1{k0}) . ']') : 'undef');
say(defined($h1{'k0'}) ? (('[' . $h1{'k0'}) . ']') : 'undef');
say(defined($h1{k0}));
say(defined($h1{k1}) ? (('[' . $h1{k1}) . ']') : 'undef');
say(defined($h1{'k1'}) ? (('[' . $h1{'k1'}) . ']') : 'undef');
say(defined($h1{k1}));
say(defined($h1{k2}) ? (('[' . $h1{k2}) . ']') : 'undef');
say(defined($h1{'k2'}) ? (('[' . $h1{'k2'}) . ']') : 'undef');
say(defined($h1{k2}));
say(defined($h1{k3}) ? (('[' . $h1{k3}) . ']') : 'undef');
say(defined($h1{'k3'}) ? (('[' . $h1{'k3'}) . ']') : 'undef');
say(defined($h1{k3}));
say(defined($h1{k4}) ? (('[' . $h1{k4}) . ']') : 'undef');
say(defined($h1{'k4'}) ? (('[' . $h1{'k4'}) . ']') : 'undef');
say(defined($h1{k4}));
say(defined($h1{k5}) ? (('[' . $h1{k5}) . ']') : 'undef');
say(defined($h1{'k5'}) ? (('[' . $h1{'k5'}) . ']') : 'undef');
say(defined($h1{k5}));
say(defined($h1{k6}) ? (('[' . $h1{k6}) . ']') : 'undef');
say(defined($h1{'k6'}) ? (('[' . $h1{'k6'}) . ']') : 'undef');
say(defined($h1{k6}));
say(defined($h1{k7}) ? (('[' . $h1{k7}) . ']') : 'undef');
say(defined($h1{'k7'}) ? (('[' . $h1{'k7'}) . ']') : 'undef');
say(defined($h1{k7}));
say(defined($h1{k8}) ? (('[' . $h1{k8}) . ']') : 'undef');
say(defined($h1{'k8'}) ? (('[' . $h1{'k8'}) . ']') : 'undef');
say(defined($h1{k8}));
say(defined($h1{k9}) ? (('[' . $h1{k9}) . ']') : 'undef');
say(defined($h1{'k9'}) ? (('[' . $h1{'k9'}) . ']') : 'undef');
say(defined($h1{k9}));
say(defined($h1{k10}) ? (('[' . $h1{k10}) . ']') : 'undef');
say(defined($h1{'k10'}) ? (('[' . $h1{'k10'}) . ']') : 'undef');
say(defined($h1{k10}));
say(defined($h1{k11}) ? (('[' . $h1{k11}) . ']') : 'undef');
say(defined($h1{'k11'}) ? (('[' . $h1{'k11'}) . ']') : 'undef');
say(defined($h1{k11}));
say(defined($h1{k12}) ? (('[' . $h1{k12}) . ']') : 'undef');
say(defined($h1{'k12'}) ? (('[' . $h1{'k12'}) . ']') : 'undef');
say(defined($h1{k12}));
say(defined($h1{nope}) ? (('[' . $h1{nope}) . ']') : 'undef');
say(defined($h1{nope}));
say(defined($h1{nope} // 'dflt') ? (('[' . ($h1{nope} // 'dflt')) . ']') : 'undef');
my $k1 = 'k1';
say(defined($h1{$k1}) ? (('[' . $h1{$k1}) . ']') : 'undef');
say(defined($h1{'k' . 2}) ? (('[' . $h1{'k' . 2}) . ']') : 'undef');
say(defined($h1{$k1 . 0}) ? (('[' . $h1{$k1 . 0}) . ']') : 'undef');
my $v1 = $h1{zz};
say($h1{k1}, $h1{k7}, $h1{k1});
say((scalar(keys(%h1)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h1{$_}) ? $h1{$_} : 'undef')) . '>' } ((sort keys(%h1))))));
my %h2 = (n => 5, s => 'ab', u => (undef), z => 0, e => "");
{
    my %t = (%h2);
    say($t{n} = 7);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{n} += 2);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{n} -= 2);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{n} *= 3);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{n} .= 'x');
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{n} x= 2);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{n} //= 9);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{n} ||= 8);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{n} &&= 6);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{n} **= 2);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{n} /= 2);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{n} %= 3);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say(++$t{n});
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{n}++);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say(--$t{n});
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{n}--);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{s} = 7);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{s} .= 'x');
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{s} x= 2);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{s} //= 9);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{s} ||= 8);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{s} &&= 6);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{u} = 7);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{u} += 2);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{u} -= 2);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{u} .= 'x');
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{u} //= 9);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{u} ||= 8);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say(++$t{u});
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{u}++);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say(--$t{u});
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{z} = 7);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{z} += 2);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{z} -= 2);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{z} *= 3);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{z} .= 'x');
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{z} x= 2);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{z} //= 9);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{z} ||= 8);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{z} &&= 6);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{z} **= 2);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{z} /= 2);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{z} %= 3);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say(++$t{z});
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{z}++);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say(--$t{z});
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{z}--);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{e} = 7);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{e} .= 'x');
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{e} x= 2);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{e} //= 9);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{e} ||= 8);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{e} &&= 6);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{new80} = 7);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{new81} += 2);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{new82} -= 2);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{new84} .= 'x');
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{new86} //= 9);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{new87} ||= 8);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say(++$t{new});
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say($t{new}++);
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
{
    my %t = (%h2);
    say(--$t{new});
    say((scalar(keys(%t)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($t{$_}) ? $t{$_} : 'undef')) . '>' } ((sort keys(%t))))));
}
say((scalar(keys(%h2)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h2{$_}) ? $h2{$_} : 'undef')) . '>' } ((sort keys(%h2))))));
my %h3;
my $i3 = 'a';
$h3{$i3} = ($i3 = 'b');
say((scalar(keys(%h3)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h3{$_}) ? $h3{$_} : 'undef')) . '>' } ((sort keys(%h3))))));
say($i3);
%h3 = ();
$i3 = 'a';
$h3{$i3} .= ($i3 = 'b');
say((scalar(keys(%h3)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h3{$_}) ? $h3{$_} : 'undef')) . '>' } ((sort keys(%h3))))));
%h3 = (a => 1);
$i3 = 'a';
$h3{$i3} += ($i3 = 5);
say((scalar(keys(%h3)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h3{$_}) ? $h3{$_} : 'undef')) . '>' } ((sort keys(%h3))))));
%h3 = ();
$h3{p} = ($h3{q} = 4);
say((scalar(keys(%h3)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h3{$_}) ? $h3{$_} : 'undef')) . '>' } ((sort keys(%h3))))));
%h3 = (n => 1);
$h3{m} = ($h3{n} + 1);
$h3{n} = ($h3{m} + $h3{n});
say((scalar(keys(%h3)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h3{$_}) ? $h3{$_} : 'undef')) . '>' } ((sort keys(%h3))))));
