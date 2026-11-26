use v5.42;
open(my $out, ">", \my $buf);
my $prev = select($out);
print "captured\n";
select($prev);
close($out);
my $ready = select(undef, undef, undef, 0);
print "[$buf][$ready]\n";
