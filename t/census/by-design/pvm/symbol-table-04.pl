use v5.42;
our $i = "before";
my @l = ($ENV{A} // "a", "b");
foreach $i (@l) { print $i }
print "\n";
print "$i\n";
