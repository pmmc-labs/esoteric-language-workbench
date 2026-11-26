use v5.42;
my $o = {}; my $c = ref($o); bless $o, "K"; my $d = ref($o); print "$c $d\n";
