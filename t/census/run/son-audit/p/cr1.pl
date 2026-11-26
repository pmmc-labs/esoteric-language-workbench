use v5.42;
my $h = {}; my $r = ref($h); bless $h, "K"; print $r, "\n";
