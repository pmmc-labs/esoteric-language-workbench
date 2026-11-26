# model: t/models/hash.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
my %h1 = (a => 1, b => 2, c => 3, d => 4);
sub all1(%o) {
    say((scalar(keys(%o)) . ':') . join(',', (map { ($_ . '=') . $o{$_} } ((sort keys(%o))))));
    return scalar(keys(%o));
}
sub one1($x, %o) {
    say($x);
    say((scalar(keys(%o)) . ':') . join(',', (map { ($_ . '=') . $o{$_} } ((sort keys(%o))))));
    return $o{k};
}
sub dflt1($x, $y = 7, %o) {
    say($x . $y);
    say((scalar(keys(%o)) . ':') . join(',', (map { ($_ . '=') . $o{$_} } ((sort keys(%o))))));
    return 1;
}
sub none1($x, %) {
    return $x;
}
sub keep1(%o) {
    $o{added} = 1;
    delete($o{a});
    return join(',', (sort keys(%o)));
}
say(all1());
say(all1(a => 1));
say(all1(a => 1, b => 2, a => 3));
say(all1(%h1));
say(all1(%h1, e => 5));
say(all1('k', ""));
say(one1(1, k => 'v'));
say(one1(2) // 'none');
say(one1(3, %h1, k => 9));
say(dflt1(1));
say(dflt1(1, 2));
say(dflt1(1, 2, a => 1));
say(dflt1(1, 2, %h1));
say(none1(1));
say(none1(1, a => 1));
say(none1(2, %h1));
say(keep1(%h1));
say((scalar(keys(%h1)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h1{$_}) ? $h1{$_} : 'undef')) . '>' } ((sort keys(%h1))))));
sub same1(%h1) {
    $h1{in} = 1;
    return scalar(keys(%h1));
}
say(same1(p => 1));
say((scalar(keys(%h1)) . ':') . join(',', (map { ((('<' . $_) . '=') . (defined($h1{$_}) ? $h1{$_} : 'undef')) . '>' } ((sort keys(%h1))))));
