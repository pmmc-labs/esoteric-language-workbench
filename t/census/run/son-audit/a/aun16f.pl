use v5.42;
my $class = "T"; sub T::DESTROY { print "d\n" } { my $o = bless {}, $class; } print "e\n";
