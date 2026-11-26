use v5.42;
my $c = $ENV{X} // 0;
if ($c == 1) { print "one\n" } elsif ($c == 0) { print "zero\n" } else { print "other\n" }
