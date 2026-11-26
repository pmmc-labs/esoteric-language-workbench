use v5.42;
my $h = {}; bless $h, "A"; my $r = ref($h); bless $h, "B"; print "$r ", ref($h), "\n";
