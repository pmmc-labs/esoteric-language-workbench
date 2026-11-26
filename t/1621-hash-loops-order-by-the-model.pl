# kind: new
# D27: a hash keeps its keys in the order they were first stored. perl's order is its own, so perl is not asked.
# model: t/models/hash.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my %h1 = (one => 1, two => 2, three => 3, four => 4);
delete($h1{two});
$h1{two} = 22;
my $t1 = "";
for my $v (values(%h1)) {
    say($v);
}
for my $v (%h1) {
    $t1 = ($t1 . $v);
}
say($t1);
for my $k (keys(%h1)) {
    say($k . $h1{$k});
    delete($h1{$k});
    $h1{$k . $k} = 1;
}
say((((join(',', keys(%h1)) . '|') . join(',', values(%h1))) . '|') . join(',', %h1));
for (values(%h1)) {
    say($_);
}
say($_) for (%h1);
say(join(',', (map { $_ . '!' } (%h1))));
say(join(',', (map { $_ + 1 } (values(%h1)))));
say(join(',', (grep { $_ ne 'oneone' } (keys(%h1)))));
say(join(',', (sort { 0 } (values(%h1)))));
say(join(',', reverse(keys(%h1))));
say(join(',', (sort { $h1{seen} = 1; $a cmp $b } (keys(%h1)))));
say((((join(',', keys(%h1)) . '|') . join(',', values(%h1))) . '|') . join(',', %h1));
my @sl1 = (@h1{'twotwo', 'oneone', 'nope'});
{
    my $dump_i = 0;
    my $dump_s = "";
    while ($dump_i < @sl1) {
        $dump_s .= (defined($sl1[$dump_i]) ? (('<' . $sl1[$dump_i]) . '>') : '<undef>');
        $dump_i++;
    }
    say((scalar(@sl1) . ':') . $dump_s);
}
say(join(',', (map { $_ } (@h1{'fourfour', 'threethree'}))));
my @d1 = (delete(@h1{'threethree', 'nope', 'oneone'}));
say(scalar(@d1));
say((((join(',', keys(%h1)) . '|') . join(',', values(%h1))) . '|') . join(',', %h1));
@h1{'z', 'y', 'twotwo', 'x'} = (26, 25, 2, 24);
say((((join(',', keys(%h1)) . '|') . join(',', values(%h1))) . '|') . join(',', %h1));
