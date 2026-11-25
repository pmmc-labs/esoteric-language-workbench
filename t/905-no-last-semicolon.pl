# The last statement of a block may leave its semicolon out, as in perl
# (D75): in a sub, a loop, an if, a bare block; before the brace on its
# line or on the next; with a modifier or without.
use v5.42;

sub double($x) { $x * 2 }
sub one() { return 1 }
sub nothing() { return }
sub sign($n) {
    return "negative" if $n < 0;
    return "zero" unless $n;
    "positive"
}
sub loud($s) { say $s }
sub count_to($n) {
    my $i = 0;
    while ($i < $n) { $i++ }
    return $i
}

say double(4);
say one();
say defined(nothing()) ? "defined" : "undef";
say sign(-2);
say sign(0);
say sign(7);
my $r = loud("said");
say $r;
say count_to(5);

my $i = 0;
while ($i < 3) { say $i; $i++ }
until ($i == 0) { $i-- }
say $i;
for (my $k = 0; $k < 2; $k++) { say "k" . $k }
if ($i == 0) { say "zero" } elsif ($i == 1) { say "one" } else { say "more" }
unless ($i) { say("unless") }
{ say "bare" }
{
    my $t = "inner";
    { $t .= "most" }
    say $t
}

# last and next, a label or none, hard before the brace.
OUTER: while (true) {
    while (true) { last OUTER }
}
$i = 0;
while ($i < 5) {
    $i++;
    if ($i == 2) { next }
    if ($i == 4) { last }
    say $i if $i > 0
}

# Whatever may end a statement: a step, an assignment, undef, a call
# with a comma after its last argument, a modifier's test.
my $u = 5;
if (true) { $u++ }
if (true) { $u = undef }
say defined($u) ? "defined" : "undef";
if (true) { $u = double(2,) }
say $u;
if (true) { say "mod" if $u == 4 }
if (true) { $u = 1 unless $u == 4 }
say $u;
sub last_is_my() { my $v = 9 }
say last_is_my();
