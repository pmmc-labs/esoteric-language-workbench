use v5.42;
package Foo;
sub new { my $c = shift; return bless {}, $c }
package main;
my $o = new Foo;
print ref $o, "\n";
