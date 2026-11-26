use v5.42;
our $g=1; sub p { print $g } { if ((local $g = 5) > 3) { p() } p(); } p(); print "\n";
