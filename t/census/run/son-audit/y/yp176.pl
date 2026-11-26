use v5.42;
our $g=1; my $o={r=>\$g}; sub t { local $g=5; ${$o->{r}} } print t(), "\n";
