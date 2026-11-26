use v5.42;
eval { eval { die "in\n" }; print "c:$@"; die "out\n" }; print "o:$@";
