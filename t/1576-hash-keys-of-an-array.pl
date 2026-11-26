# kind: refused
# perl's keys takes it, for the indexes: 3. Not in the language.
use v5.42;
my @a = (1, 2, 3);
say scalar(keys @a);
