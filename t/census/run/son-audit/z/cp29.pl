use v5.42;
my $s="abc"; my $t=$s; substr($s,0,1)="z"; print "$t$s\n";
