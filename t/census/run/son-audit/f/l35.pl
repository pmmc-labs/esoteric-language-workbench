use v5.42;
our $s=""; my $r=\$s; for (1..3) { $$r.=$_; $s.="-" } print "$s\n";
