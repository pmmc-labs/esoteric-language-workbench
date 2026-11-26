use v5.42;
package Foo;
sub hi { return "hi" }
package main;
print Foo->hi, "\n";
