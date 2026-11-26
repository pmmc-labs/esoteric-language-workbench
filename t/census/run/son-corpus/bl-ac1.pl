use v5.42;
my $r = [1]; my $e = []; print((@$r ? "y" : "n"), (@$e ? "y" : "n"), "\n"); if (@$r) { print "ok\n" }
