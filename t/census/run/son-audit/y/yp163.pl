use v5.42;
our $g=1; my $r=\$g; sub p { $$r } { local $g=5; print p(), $g } print "\n";
