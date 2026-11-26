use v5.42;
package Foo;
sub hi { return "called" }
package main;
my $o = bless {}, $ENV{X} // "Foo";
print $o->can("hi")->($o), "\n";
