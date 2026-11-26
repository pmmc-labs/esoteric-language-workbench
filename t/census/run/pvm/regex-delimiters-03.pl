use v5.42;
my $hit = "a{b}c" =~ m{a{b}c};
my $s = "xa{b}cy";
$s =~ s{a{b}c}{ok};
print "[$hit][$s]\n";
