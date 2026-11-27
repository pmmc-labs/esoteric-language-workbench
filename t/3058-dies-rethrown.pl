# kind: dies
# die $e: the message unchanged, its first place kept (T305).
use v5.42;
say 1;
try {
    die "where";
} catch ($e) {
    say 2;
    die $e;
}
