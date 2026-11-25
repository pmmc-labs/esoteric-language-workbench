use v5.42;
my @x = (7, 8);
my $y = $#x# a comment, to perl
;
say $y;
say $#x -1;
my @r = (1..3);
say scalar(@r);
@r = (1...3);
say scalar(@r);
@r = (1.5..3);
say scalar(@r), " ", $r[0];
say $x [1];
my $x = 5;
say $x [1];
