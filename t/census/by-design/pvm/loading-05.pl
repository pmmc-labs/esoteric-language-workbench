use v5.42;
my $m = "warnings.pm";
require $m;
print "loaded ", ($INC{$m} ? "yes" : "no"), "\n";
