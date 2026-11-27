# Which line a message names (D34, D150, T302, T318): the line its statement
# is on; a test's, its keyword's; a default's, its parameter's; a message
# written to end in a newline over several lines.
use v5.42;
my $x;
try {
    if (0) { say 0 }
    elsif ($x // die "elsif") { say 1 }
} catch ($e) { print $e }
try { for my $i (1, $x // die "for") { say $i } } catch ($e) { print $e }
sub f($p,
      $q = die "default") {
    return $p;
}
try {
    f(
        2);
} catch ($e) { print $e }
my @m;
try {
    @m = map {
        die "in the block" if $_ == 2;
        $_ } (1, 2);
} catch ($e) { print $e }
try {
    die "over ",
        "two lines\n";
} catch ($e) { print $e }
my $i = 0;
try { while ($i < 2 || die "loop ended\n") { $i++ } } catch ($e) { print $e }
sub g() {
    die "in g";
}
try {
    say "a",
        g();
} catch ($e) { print $e }
try { die "first" } catch ($e) { print $e } try { die "same line" } catch ($e) { print $e }
