use v5.42;
use v5.36;
package Foo;
package Bar;
package main;
my $o = bless {}, $ENV{X} // "Foo";
my $yes = $o isa Foo;
my $no = $o isa Bar;
print "$yes$no|\n";
