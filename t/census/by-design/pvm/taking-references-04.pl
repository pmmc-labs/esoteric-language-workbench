use v5.42;
use feature "switch";
my $x = $ENV{X} // 3;
my @l = (2, 3);
given ($x) {
    when (@l) { print "listed\n" }
    default { print "unlisted\n" }
}
