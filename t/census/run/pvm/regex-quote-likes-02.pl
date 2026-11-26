use v5.42;
my $s = $ENV{X} // "a.c";
my $t = $s;
my $n = ($t =~ tr/./Z/);
my $u = $s;
$u =~ s/./Z/;
print "$t $n $u\n";
