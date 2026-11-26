use v5.42;
use POSIX;
use Fcntl ();
use constant TAG => "c";
END { print "end\n" }
BEGIN { print "begin\n" }
package Greet;
sub hello { return "hello" }
sub import { print "import $_[1]\n" }
package Louder {
    sub shout { return "HELLO" }
}
package main;
require strict;
my $mod = "warnings.pm";
require $mod;
Greet->import("tag");
print Greet::hello(), " ", Louder::shout(), "\n";
print "inc: ", ($INC{"strict.pm"} ? "yes" : "no"), ($INC{"warnings.pm"} ? "yes" : "no"), "\n";
print "use: ", ($main::{"floor"} ? "yes" : "no"), ($main::{"LOCK_EX"} ? "yes" : "no"), "\n";
#line 300 "adj"
print "pkg ", __PACKAGE__, " line ", __LINE__, " file ", __FILE__, " tag ", TAG, "\n";
