use v5.42;
our $g=1; sub r { ($g, $g++) } my @l=r(); print "@l\n";
