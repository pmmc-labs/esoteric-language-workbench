use v5.42;
my $s="aa"; (my $t=$s)=~s/(a)/<$1>/g; "b"=~/(b)/; print "$t$1\n";
