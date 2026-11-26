use v5.42;
package Marker;
sub import { print "import $_[0] $_[1]\n" }
package main;
Marker->import("tag");
print "after\n";
