use v5.42;
sub f { defer { print "D\n" } print "body\n" }
eval { f() };
print "end\n";
