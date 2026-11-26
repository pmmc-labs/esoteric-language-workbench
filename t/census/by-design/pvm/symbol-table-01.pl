use v5.42;
my $n = $ENV{X} // 3;
*sq = sub { $_[0] * $_[0] };
print sq($n), " ", $n * 2, "\n";
