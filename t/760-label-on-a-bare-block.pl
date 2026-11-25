# kind: refused
# perl takes it, and last L leaves the block: it prints after (T121).
use v5.42;
L: {
    last L;
    say "not reached";
}
say "after";
