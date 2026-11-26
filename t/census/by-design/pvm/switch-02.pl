use v5.42;
use feature "switch";
my $x = $ENV{X} // 9;
given ($x) {
    when (1) { print "one\n" }
    default { print "other\n" }
}
print "after\n";
