# kind: warns
# A warn in a try is said at once, and a die after it still caught.
use v5.42;
sub check($n) {
    warn "checking $n\n";
    die "bad $n\n" if $n % 2;
    return "good $n";
}
for my $n (1 .. 4) {
    try { say check($n) } catch ($e) { warn "caught: $e" }
}
