# kind: refused
# perl does not compile it: Bareword 'a' not allowed while 'strict subs' in use.
use v5.42;
my $h = {a => 1};
say $h->{
a};
