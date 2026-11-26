use v5.42;
my $s="a"; sub n { $s.="b"; "" } my $r = $s . n() . $s; print "$r\n";
