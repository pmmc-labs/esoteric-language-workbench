use v5.42;
my $d; $d--; my $s="a"; $s--; my $e=""; $e++; my $f="a-b"; { no warnings; $f++; } print "$d $s $e $f\n";
