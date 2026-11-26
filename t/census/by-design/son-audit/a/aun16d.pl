use v5.42;
sub DESTROY { print "d" } sub mk { bless [], "main" } mk(); print "e\n";
