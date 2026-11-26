use v5.42;
my @a=(1,2,3); sub n { @a=(); 0 } my $r = n() + @a; print "$r\n";
