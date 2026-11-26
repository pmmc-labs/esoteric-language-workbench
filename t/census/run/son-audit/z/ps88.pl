use v5.42;
my $str="a,b,c"; my $n=0; $n++ while $str=~/,/g; print "$n\n";
