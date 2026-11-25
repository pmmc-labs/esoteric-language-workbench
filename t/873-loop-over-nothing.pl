# kind: refused
# perl does not compile it (T155).
use v5.42;
for my $x () {
    say "never";
}
