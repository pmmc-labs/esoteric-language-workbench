use v5.42;
our $g="a"; sub f { $g="b"; "x" } my $v = "$g@{[f()]}$g"; print "$v\n";
