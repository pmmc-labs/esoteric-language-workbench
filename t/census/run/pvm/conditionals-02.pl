use v5.42;
my $c = $ENV{X} // 0;
unless ($c) { print "block\n" }
print "postfix\n" unless $c;
