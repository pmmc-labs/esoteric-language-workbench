use v5.42;
our $g=1; our $r=\$g; local $g=5; print "$$r$g\n";
