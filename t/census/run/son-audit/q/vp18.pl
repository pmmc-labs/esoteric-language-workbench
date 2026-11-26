use v5.42;
my %h = (a=>1); my ($d, $e) = (delete $h{a}, exists $h{a} ? "y" : "n"); print "$d $e\n";
