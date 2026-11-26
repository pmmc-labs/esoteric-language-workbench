use v5.42;
my %P = (a => "b", b => "c");
my $cur = "a"; my $s = "";
while (my $next = $P{$cur}) { $s .= $next; $cur = $next }
print "$s\n";
