# model: t/models/ref.py
use v5.42;
{
    my $r;
    $r->{a}{b}[2] = 1;
    say(ref($r));
    say(defined($r->{a}->{b}[2]) ? $r->{a}->{b}[2] : "u");
    say(defined($r->{a}{b}->[0]) ? $r->{a}{b}->[0] : "u");
    say(defined($r->{a}{b}[3]) ? $r->{a}{b}[3] : "u");
    say(ref($r->{a}->{b}));
    $r->{a}{c} = "x";
    $r->{list}[3]->{k} = 2;
    say(defined($r->{a}{c}) ? $r->{a}{c} : "u");
    say(defined($r->{list}[0]) ? $r->{list}[0] : "u");
    say(ref($r->{list}->[3]));
    say(defined($r->{list}[3]{k}) ? $r->{list}[3]{k} : "u");
    say(defined($r->{list}->[-1]{k}) ? $r->{list}->[-1]{k} : "u");
}
{
    my $q;
    $q->[1][0]->{x} = 7;
    say(defined($q->[1][0]{x}) ? $q->[1][0]{x} : "u");
    say(defined($q->[0]) ? $q->[0] : "u");
    say(defined($q->[1]->[1]) ? $q->[1]->[1] : "u");
    say(defined($q->[-1][0]{x}) ? $q->[-1][0]{x} : "u");
    $q->[-2] = "first";
    $q->[1]->[0]{y} = [8, 9];
    say(defined($q->[0]) ? $q->[0] : "u");
    say(defined($q->[1][0]->{y}[1]) ? $q->[1][0]->{y}[1] : "u");
    say(ref($q->[1][0]->{y}));
}
{
    my $s = [1, [2, 3], {k => "v", n => [4, undef]}, undef, "end"];
    my $t = {a => {b => {c => 5}}, list => [[6, 7], [8]], u => undef, z => 0};
    my $u = [[[[9]]]];
    my $v = {x => [{y => [10, 11]}]};
    $s->[1][5] = 12;
    $s->[2]{n}->[1] = "set";
    $s->[3]{made} = 13;
    $s->[2]{new}->[0] = 14;
    say(defined($s->[1][5]) ? $s->[1][5] : "u");
    say(defined($s->[1][4]) ? $s->[1][4] : "u");
    say(defined($s->[1]->[2]) ? $s->[1]->[2] : "u");
    say(defined($s->[2]{n}[1]) ? $s->[2]{n}[1] : "u");
    say(defined($s->[3]->{made}) ? $s->[3]->{made} : "u");
    say(defined($s->[2]{new}[0]) ? $s->[2]{new}[0] : "u");
    say(defined($s->[4]) ? $s->[4] : "u");
    $t->{a}->{b}{d} = 15;
    $t->{u}[0] = 16;
    $t->{list}->[1][1] = 17;
    say(defined($t->{a}{b}->{d}) ? $t->{a}{b}->{d} : "u");
    say(defined($t->{a}{b}{c}) ? $t->{a}{b}{c} : "u");
    say(defined($t->{u}->[0]) ? $t->{u}->[0] : "u");
    say(defined($t->{list}[1][0]) ? $t->{list}[1][0] : "u");
    say(defined($t->{list}->[1][1]) ? $t->{list}->[1][1] : "u");
    $u->[0][0]->[0][1] = 18;
    $u->[0][1]->[0][0] = 19;
    say(defined($u->[0][0]->[0][0]) ? $u->[0][0]->[0][0] : "u");
    say(defined($u->[0][0]->[0][1]) ? $u->[0][0]->[0][1] : "u");
    say(defined($u->[0][1]->[0][0]) ? $u->[0][1]->[0][0] : "u");
    say(ref($u->[0][1]->[0]));
    $v->{x}[0]{y}->[2] = 20;
    $v->{x}[1]{y}->[0] = 21;
    say(defined($v->{x}[0]{y}->[2]) ? $v->{x}[0]{y}->[2] : "u");
    say(defined($v->{x}[0]{y}->[1]) ? $v->{x}[0]{y}->[1] : "u");
    say(defined($v->{x}[1]{y}->[0]) ? $v->{x}[1]{y}->[0] : "u");
    say(ref($v->{x}[1]{y}));
}
{
    my @a;
    my %h;
    $a[3]->[0] = 1;
    say(scalar(@a));
    $a[0]{k} = 2;
    $a[-1][1] = 3;
    say(scalar(@a));
    say(defined($a[3]->[0]) ? $a[3]->[0] : "u");
    say(defined($a[3][1]) ? $a[3][1] : "u");
    say(defined($a[0]{k}) ? $a[0]{k} : "u");
    say(defined($a[1]) ? $a[1] : "u");
    say(defined($a[-4]->{k}) ? $a[-4]->{k} : "u");
    $h{x}{y}{z} = 4;
    $h{w}->[2] = 5;
    $h{x}{v} = 6;
    say(join(",", sort keys(%h)));
    say(defined($h{x}{y}->{z}) ? $h{x}{y}->{z} : "u");
    say(defined($h{x}{v}) ? $h{x}{v} : "u");
    say(defined($h{w}[2]) ? $h{w}[2] : "u");
    say(defined($h{w}->[0]) ? $h{w}->[0] : "u");
    say(ref($h{x}{y}));
}
