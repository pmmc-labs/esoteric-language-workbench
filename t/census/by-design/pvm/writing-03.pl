use v5.42;
use feature "say";
my $line = $ENV{X} // "said";
open(my $out, ">", \my $buf);
say $out $line;
print $out "printed";
close($out);
print "[$buf]\n";
