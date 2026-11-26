use v5.42;
my $s="ab"; sub f { "@_" } print f($s, $s=~s/a/z/), "\n";
