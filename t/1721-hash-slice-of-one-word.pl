# kind: refused
# perl warns of it too, and the word is the key a.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
say @h{a};
