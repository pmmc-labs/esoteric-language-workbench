use v5.42;
my $t = "a.c";
my $c = ($t =~ tr/./Z/);
print "mid $t\n";
print "end $c\n";
