use v5.42;
my $s = "aaa";
my $n = ($s =~ s/a/b/g);
print "mid $s\n";
print "end $n\n";
