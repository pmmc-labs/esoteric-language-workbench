# Is "$x" ever anything a later operation can tell from $x . "" ?
# For each kind of value and each way of writing it into a string, everything a
# later operation can see; a line is printed only where two ways differ.
# Run: /opt/perl-5.42/bin/perl same-as-dot.pl   (prints "N values, M differ")
use v5.42;
no warnings 'experimental::builtin';
my @vals = (
    0, 1, -1, 7, 9007199254740992, 9007199254740993, 9223372036854775807, -9223372036854775808,
    0.5, 3.0, -0.0, 0.0 * -1, 1e15, 1e16, 1e21, 0.1 + 0.2, 1 / 3, 1e300, 2 ** 53, 2 ** 62, 2 ** 64, -17 / 4,
    true, false, !1, !0, (1 == 1), "", "0", "00", "0.0", "3.0", " 3", "3 ", "0 but true", "abc", "12abc", "1e3", "0x10",
    "-0", "+3", "-", "a9", "Az", "zz", "a", "09", "9007199254740993", "1_000", ".5", "5.", "0e0", "Inf", "NaN", "\n", "\x{e9}", "\x{263A}",
);
push @vals, 1 . "", "3" + 0, "3.0" + 0, 10 / 2, 2 ** 10, 9 ** 20, int(7.9), -(-0.0);
{ my $n = 5; my $t = "$n"; push @vals, $n; }             # a number that has been a string
{ my $s = "42"; my $t = $s + 0; push @vals, $s; }        # a string that has been a number
{ my $s = "4.0"; my $t = $s + 0; push @vals, $s; }
{ my $s = "abc"; { no warnings; my $t = $s + 0; } push @vals, $s; }
my $w = "";
local $SIG{__WARN__} = sub ($m) { $m =~ s/ at .*//s; $w .= "{$m}" };
sub see ($s) {
    my @o;
    $w = "";
    push @o, "bool=" . (builtin::is_bool($s) ? 1 : 0);
    push @o, "num=" . (builtin::created_as_number($s) ? 1 : 0);
    push @o, "str=[$s]";
    push @o, "len=" . length($s);
    push @o, "truth=" . ($s ? "t" : "f");
    { my $c = $s; $c++; push @o, "++=[$c]"; }
    { my $c = $s; $c--; push @o, "--=[$c]"; }
    { my $c = $s; push @o, "+0=[" . ($c + 0) . "]"; }
    { my $c = $s; push @o, "neg=[" . (-$c) . "]"; }
    { my $c = $s; push @o, "*1=[" . ($c * 1) . "]"; }
    { my $c = $s; push @o, "==1:" . (($c == 1) ? 1 : 0); }
    { my $c = $s; push @o, "eq1:" . (($c eq "1") ? 1 : 0); }
    { my $c = $s; push @o, "<=>:" . ($c <=> 2); }
    { my $c = $s; my @z = (10, 11, 12, 13); push @o, "idx=" . ($z[$c] // "U"); }
    { my $c = $s; my $big; { no warnings; $big = $c > 1000; } push @o, "x=" . ($big ? "big" : length("ab" x $c)); }
    { my $c = $s; push @o, "sub=" . (eval { substr("abcdef", $c, 1) } // "U"); }
    { my $c = $s; push @o, "cat=[" . ($c . $c) . "]"; }
    { my $c = $s; push @o, "after+0 str=[$c]"; }
    return join(" ", @o) . " warn=$w";
}
my ($n, $bad) = (0, 0);
for my $v (@vals) {
    my $x = $v;
    my @a = ($v);
    my @b = ($v, $v);
    my %form = (
        'dot'      => $x . "",
        '"$x"'     => "$x",
        '"${x}"'   => "${x}",
        '"$a[0]"'  => "$a[0]",
        '"@a"'     => "@a",
        'join'     => join(" ", @a),
        '"@{a}"'   => "@{a}",
    );
    my $s2 = "@b[0, 0]"; my $j2 = join(" ", @b[0, 0]); my $d2 = $v . " " . $v;
    my $e = "$x$x"; my $de = $x . $x;
    my $base = see($form{dot});
    $n++;
    my $diff = 0;
    for my $k (sort keys %form) {
        my $got = see($form{$k});
        if ($got ne $base) { $diff = 1; say "DIFFER for [$v] as $k:\n  dot: $base\n  got: $got"; }
    }
    if (see($s2) ne see($j2) or see($s2) ne see($d2)) { $diff = 1; say "DIFFER for [$v] in a slice"; }
    if (see($e) ne see($de)) { $diff = 1; say "DIFFER for [$v] doubled"; }
    $bad += $diff;
}
say "$n values, $bad differ";
