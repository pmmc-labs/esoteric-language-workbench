use v5.42;
package Foo;
sub hi { return "hi" }
package main;
my $o = bless {}, "Foo";
my $m = "hi";
print $o->$m, "\n";
