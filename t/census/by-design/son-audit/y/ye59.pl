use v5.42;
our $g="ab"; sub f { "@_" } print f($g, scalar($g =~ s/a/z/)), "\n";
