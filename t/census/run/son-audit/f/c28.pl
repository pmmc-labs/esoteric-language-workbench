use v5.42;
my $s="abc"; (my $t=$s)=~tr/a-c/A-C/; print "$s $t\n";
