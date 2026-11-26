# model: t/models/hash.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my %h1 = (a => 1, b => 'two', c => 0.5, d => true, e => "", if => 'word', k1 => 'n');
my $k1 = 'b';
say("$h1{a}");
say("a=$h1{a}, b=$h1{$k1}.");
say("$h1{a}$h1{b}$h1{c}$h1{d}$h1{e}$h1{if}");
say("[$h1{e}]");
say("$h1{a} [0]");
say("$h1{a}->x");
say("$h1{a}(1)");
say("$h1{a}-$h1{a}");
say("$h1{k1}$h1{$k1}");
say("%h1 $h1{a} %");
$k1 = 'c';
say("$h1{$k1} $k1 $h1{b}");
my $s1 = "$h1{a}+$h1{a}";
say($s1);
say("$h1{a}" . "$h1{b}");
say(length("$h1{b}$h1{b}"));
$h1{a} = "$h1{a}$h1{a}";
say($h1{a});
$h1{"$h1{b}!"} = 1;
say((scalar(keys(%h1)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h1{$_}) ? $h1{$_} : 'undef')) . '>' } ((sort keys(%h1))))));
for my $x ((sort keys(%h1))) {
    say("$x=$h1{$x}");
}
say(join(',', (map { "<$h1{$_}>" } ((sort keys(%h1))))));
