use v5.42;
my $t = "a.c";
my $c = ($t =~ tr/./Z/);
print "both $t $c\n";
