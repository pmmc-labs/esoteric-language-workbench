use v5.42;
use feature "switch";
my $x = $ENV{X} // 7;
given ($x) {
    when ($_ > 5) { print "big\n" }
    default { print "small\n" }
}
