# kind: refused
# perl reads the key 1, and warns of the undef it finds there (T223).
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
say $h{
  true
};
