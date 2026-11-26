use v5.42;
eval { die "a\n" } or print "caught $@";
