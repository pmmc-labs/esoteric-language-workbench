use v5.42;
my $c = $ENV{X} // 1;
if ($c) { print "block\n" }
print "postfix\n" if $c;
