use v5.42;
my $c = $ENV{X} // 0;
if ($c) { print "taken\n" } else { print "else\n" }
