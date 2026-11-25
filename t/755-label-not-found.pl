# kind: refused
# perl prints before, and dies when the last runs: Label not found for
# "last NOPE" (T121, D61).
use v5.42;
my $i = 0;
say "before";
while ($i++ < 3) {
    last NOPE;
}
