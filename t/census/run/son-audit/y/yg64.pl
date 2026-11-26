use v5.42;
my $t = "The quick brown fox"; print ucfirst(join(" ", map { ucfirst } reverse split / /, lc $t)), "\n";
