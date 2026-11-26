use v5.42;
my ($a,$b)=(1,2); my $c=@ARGV==0; my $r = $c ? \$a : \$b; $$r=9; print "$a$b\n";
