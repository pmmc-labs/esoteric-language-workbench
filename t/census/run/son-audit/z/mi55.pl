use v5.42;
my $s="abc"; print $s=~/b/ ? "$`|$&|$'" : "no", "\n";
