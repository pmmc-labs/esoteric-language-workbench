use v5.42;
use File::Spec::Functions qw(catfile splitpath); print catfile("a", "b"), " ", join("|", splitpath("/d/e/f.txt")), "\n";
