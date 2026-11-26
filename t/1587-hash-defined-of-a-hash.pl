# kind: refused
# perl dies: Can't use 'defined(%hash)' (Maybe you should just omit the defined()?).
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
say defined(%h) ? 1 : 0;
