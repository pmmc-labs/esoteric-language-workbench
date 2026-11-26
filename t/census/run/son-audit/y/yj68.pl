use v5.42;
INIT { print "i" } CHECK { } BEGIN { print "b" } print "r"; END { print "e\n" }
