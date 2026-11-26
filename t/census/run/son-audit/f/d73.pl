use v5.42;
our $g=1; sub f { local $g=2; nosuch() } eval { f() }; print "$g ", $@?1:0, "\n";
