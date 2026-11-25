# kind: refused
# perl tests the reversed string.
use v5.42;
my @a = (1, 2);
if (reverse(@a)) {
    say 1;
}
