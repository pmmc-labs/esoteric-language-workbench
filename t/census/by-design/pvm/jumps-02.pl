use v5.42;
my $c = $ENV{X} // 0;
my $t = $ENV{T} // "TAIL";
print "a";
goto SKIP unless $c;
print "b";
SKIP:
print "c";
goto $t;
print "d";
TAIL:
print "e\n";
