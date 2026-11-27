# model: t/models/ref.py
use v5.42;
sub total($t) {
    return $t->[0] + $t->[1];
}
sub make($n) {
    return { n => $n, l => [$n, $n * 2] };
}
sub mark($p) {
    $p->[0] = 1;
    return ref($p);
}
sub pair() {
    return ([1], {k => 2});
}
sub add_to($l, $v) {
    $l->[0] += $v;
    return;
}
{
    my @rows = ([1, "a"], [2, "b"], [3, "c"]);
    for my $row (@rows) {
        say($row->[0], $row->[1]);
}
for (@rows) {
    $_->[0] *= 10;
}
say($rows[0][0], $rows[2][0]);
my @recs = ({n => 3, name => "c"}, {n => 1, name => "a"}, {n => 2, name => "b"});
say(join(",", map { $_->{name} } sort { $a->{n} <=> $b->{n} } @recs));
say(join(",", map { $_->{n} } grep { $_->{name} ne "b" } @recs));
say(join(",", map { $_->[0] } sort { $b->[0] <=> $a->[0] } @rows));
my $r = [7, 8, 9];
for my $x ($r->[0], $r->[2]) {
    say($x);
}
my %by = (a => [1, 2], b => [3]);
for my $k (sort keys(%by)) {
    say($k, $by{$k}[0], defined($by{$k}[1]) ? $by{$k}[1] : "u");
}
say(join(",", map { $_ * 2 } ($r->[0], $r->[1])));
my $total = 0;
$total += $_->[0] for @rows;
say($total);
}
{
say(total([3, 4]));
say(make(5)->{l}[1], make(6)->{n});
my $m = make(2);
$m->{l}[0] = 9;
say($m->{l}[0], make(2)->{l}[0]);
my $u;
say(mark($u), defined($u) ? 1 : 0);
my $w = [0];
mark($w);
say($w->[0]);
my @p = pair();
say($p[0][0], $p[1]{k});
my $acc = [1];
add_to($acc, 4);
say($acc->[0]);
}
