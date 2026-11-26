use v5.42;
sub f { "@_" } my @a=(1,2); my @b=(3); print f(@a, @b), "|", f(\@a == \@a ? "same" : "diff"), "|", f(scalar(@a), "@b"), "\n";
