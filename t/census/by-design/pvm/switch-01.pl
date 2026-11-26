use v5.42;
use feature "switch";
my $x = $ENV{X} // 2;
given ($x) {
    when (1) { print "one\n" }
    when (2) { print "two\n" }
    default { print "other\n" }
}
