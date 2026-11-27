# kind: same
# chomp leaves a reference as it is, as perl does (T279's kin, step 13a).
use v5.42;
my $r = [1, 2];
chomp($r);
say ref($r), $r->[1];
my $h = {};
chomp $h;
$h->{k} = 3;
say ref $h, $h->{k};
