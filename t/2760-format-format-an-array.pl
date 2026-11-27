# kind: refused
# perl takes the count for the format: 3 (T22, T274).
use v5.42;
my @a = ("%s-%s", 2, 3);
say sprintf(@a);
