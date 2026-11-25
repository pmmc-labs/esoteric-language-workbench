# kind: fault
# A wrong number of arguments names the line the statement begins on, as
# perl does (line 12 here), after every argument has been worked out.
use v5.42;
sub two($p, $q) {
    return $p . $q;
}
sub loud($p) {
    say $p;
    return $p;
}
say two(
    loud("a"),
    loud("b"),
    loud("c"),
);
say "not reached";
