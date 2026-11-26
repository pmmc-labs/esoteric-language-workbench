use v5.42;
my $h={a=>1}; sub ad { $_[0]{b}=2 } my %c=%$h; ad($h); print scalar(keys %c),"\n";
