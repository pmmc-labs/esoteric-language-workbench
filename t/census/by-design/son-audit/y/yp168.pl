use v5.42;
our $g=1; my @l = ($g, local $g = 5); print "@l\n";
