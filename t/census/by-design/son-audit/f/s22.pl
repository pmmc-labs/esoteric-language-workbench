use v5.42;
my $i=0; sub n { ++$i } my $s=n().n().n(); print "$s\n";
