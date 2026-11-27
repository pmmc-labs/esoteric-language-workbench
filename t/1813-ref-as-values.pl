# model: t/models/ref.py
use v5.42;
sub fresh() {
    my %h = (n => 1);
    return \%h;
}
{
    my $r = [1, 2];
    my $s = $r;
    my $t = [1, 2];
    say($r == $s ? 1 : 0);
    say($r == $t ? 1 : 0);
    say($r != $t ? 1 : 0);
    say([] == [] ? 1 : 0);
    my @a = (5);
    my %h = (k => 6);
    my $ra = \@a;
    my $rh = \%h;
    say($ra == \@a ? 1 : 0);
    say(\@a == \@a ? 1 : 0);
    say($rh == \%h ? 1 : 0);
    $a[1] = 7;
    say($ra->[1]);
    $ra->[2] = 8;
    say(scalar(@a));
    $rh->{j} = 9;
    say(join(",", sort keys(%h)));
    say($h{j});
}
{
    my $r = [1];
    my $h = {};
    my $u;
    my $n = 3;
    my $s = "ARRAY";
    say("[", ref($r), "]");
    say("[", ref($h), "]");
    say("[", ref($u), "]");
    say("[", ref($n), "]");
    say("[", ref($s), "]");
    say("[", ref([]), "]");
    say("[", ref({}), "]");
    say(ref $r eq "ARRAY" ? 1 : 0);
    say(ref($h) eq "HASH" ? 1 : 0);
    say($r ? "t" : "f", $h ? "t" : "f", !$r ? "t" : "f");
    say(defined($r) ? 1 : 0, defined($u) ? 1 : 0);
    say($u // $r == $r ? 1 : 0);
    say(($r || 0) == $r ? 1 : 0);
    say(!!$h ? "t" : "f");
}
{
    my @rows = ([1, 2], [3, 4]);
    my @c = @rows;
    $c[0][0] = 9;
    $c[1] = [5];
    say($rows[0][0], $rows[1][0], $c[1][0]);
    my @d = ([0]) x 2;
    $d[0][0] = 5;
    say($d[1][0], $d[0] == $d[1] ? 1 : 0);
    my @a = (1, 2);
    my $c = [@a];
    $a[0] = 7;
    say($c->[0], $a[0]);
    my @one = [1, 2, 3];
    say(scalar(@one), $one[0][2]);
    say(+{a => 1, a => 2}->{a});
    my %g = (x => [1]);
    my %f = %g;
    $f{x}[0] = 2;
    say($g{x}[0]);
    my $deep = {a => [1, {b => 2}]};
    my $copy = $deep->{a};
    $copy->[1]{b} = 3;
    say($deep->{a}[1]{b});
}
{
    my $q = {n => 1};
    $q->{self} = $q;
    say($q->{self}{self}{n}, $q->{self} == $q ? 1 : 0);
    my $x = [1];
    my $y = [$x];
    $x->[1] = $y;
    say($x->[1][0][1][0][0]);
    for my $k (1 .. 3) {
        my $c = {k => $k};
        $c->{me} = $c;
}
my $z;
$z->[0] = $z;
say($z->[0][0] == $z ? 1 : 0);
}
{
my $r = {a => {b => 1, c => undef}, l => [{k => 2}]};
my %h = (x => {y => 3});
say(exists($r->{a}{b}) ? 1 : 0, exists($r->{a}{c}) ? 1 : 0, exists($r->{a}{d}) ? 1 : 0);
say(exists $r->{l}[0]{k} ? 1 : 0, exists($h{x}{y}) ? 1 : 0, exists $h{x}->{z} ? 1 : 0);
say(delete($r->{a}{b}), exists($r->{a}{b}) ? 1 : 0);
my $d = delete $h{x}{y};
say($d, exists($h{x}{y}) ? 1 : 0, exists($h{x}) ? 1 : 0);
say(defined(delete($r->{a}{nope})) ? 1 : 0);
delete $r->{l}[0]{k};
say(exists($r->{l}[0]{k}) ? 1 : 0);
}
{
my @r;
for my $i (1 .. 3) {
    my @a = ($i);
    push @r, \@a;
}
say($r[0][0], $r[1][0], $r[2][0]);
my $f = fresh();
my $g = fresh();
$f->{n} = 2;
say($g->{n}, $f == $g ? 1 : 0);
}
