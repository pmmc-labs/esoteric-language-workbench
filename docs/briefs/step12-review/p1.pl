use v5.42;
# P1: keys and values are named unary operators too: T220's rule names
# only exists and delete. perl does not compile this file; each line alone
# fails the same way.
my %h = (a => 1, b => 2);
say keys %h + 1;
say values %h * 2;
say keys %h . " keys";
say keys %h x 2;
say keys(%h) + 1;        # fine: 3
say keys %h == 2;        # fine: a comparison binds looser
