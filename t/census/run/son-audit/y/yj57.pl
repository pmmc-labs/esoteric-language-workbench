use v5.42;
$_ = "x"; my @r = grep { $_ ne "b" } map { lc } qw(A B C); print "@r$_\n";
