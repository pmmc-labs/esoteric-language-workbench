use v5.42;
use POSIX ();
print "POSIX loaded: ", ($INC{"POSIX.pm"} ? "yes" : "no"), "\n";
print "floor imported: ", ($main::{"floor"} ? "yes" : "no"), "\n";
