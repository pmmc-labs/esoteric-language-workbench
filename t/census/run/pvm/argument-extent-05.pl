use v5.42;
my $n = $ENV{N} // 7;
lock($n);
print "locked ", $n, "\n";
