# kind: refused
# perl runs it: '1\n'.
use v5.42;
my %g = (a => {b => 1});
say "$g{a}{b}";
