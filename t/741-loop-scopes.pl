# Which variable a name means in and round a loop: a loop is a scope for
# its test or its first part, its block is another inside that, and each
# is gone after the loop (T119, D62).
use v5.42;
my $x = "outer";
my $i = 0;
while ((my $x = $i++) < 2) {
    say "test's: " . $x;
    my $x = "block's";
    say $x;
}
say $x;
until ((my $x = $i--) <= 1) {
    say "until's: " . $x;
}
say $x;
for (my $x = 0; $x < 2; $x++) {
    say "for's: " . $x;
    my $x = "block's again";
    say $x;
}
say $x;
my $k = 5;
for (my $k = $k + 1, my $m = $k * 2; $k < $m; $k += 2) {
    say $k . " and " . $m;
}
say $k;
for (my $k = 0; $k < 2; $k++) {
    for (my $k = 10; $k < 12; $k++) {
        say "inner " . $k;
    }
    say "outer " . $k;
}
$i = 0;
while ($i++ < 2) {
    my $x;
    say defined $x ? "defined" : "undef";
    $x = "set";
    {
        my $x;
        say defined $x ? "defined" : "undef";
        $x = "set too";
    }
    if ($i) {
        my $x;
        say defined $x ? "defined" : "undef";
        $x = "and here";
    }
}
$i = 0;
my $kept = "";
while ($i++ < 3) {
    my $fresh = "";
    $kept .= $i;
    $fresh .= $i;
    say $kept . " " . $fresh;
}
$i = 0;
while ($i++ < 3) {
    next if $i == 2;
    my $after_next;
    $after_next .= "a";
    say $after_next;
}
$i = 0;
L: while ($i++ < 2) {
    my $j = 0;
    while ((my $both = $i . $j) && $j++ < 2) {
        next L if $j == 2;
        say $both;
    }
}
for (my $n; ($n // 0) < 2; $n++) {
    say defined $n ? $n : "undef";
}
say $x;
