use v5.42;
our $g; my $v = ($g //= 3); $g++; print "$v$g\n";
