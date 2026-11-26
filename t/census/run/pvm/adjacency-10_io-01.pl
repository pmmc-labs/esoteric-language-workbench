use v5.42;
use feature "say";
open(my $in, "<", \"first\nsecond\nthird\n");
my $head = <$in>;
my @rest = <$in>;
print STDOUT $head;
print STDOUT scalar(@rest), " left, eof ", (eof($in) ? "yes" : "no"), "\n";
print STDOUT join("", reverse @rest);
close($in);
open(my $out, ">", \my $buf);
my $prev = select($out);
say "round trip";
select($prev);
close($out);
my $ready = select(undef, undef, undef, 0);
our $AUTOLOAD;
sub AUTOLOAD { my $n = $AUTOLOAD; $n =~ s/.*:://; return "auto:$n" }
*sq = sub { $_[0] * $_[0] };
print $buf, "ready $ready sq ", sq(3), " glob ", ref(\*STDOUT), " ", missing(), "\n";
