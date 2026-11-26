use v5.42;
our $g = 1; *h = \$g; our $h; $h = 5; print "$g\n";
