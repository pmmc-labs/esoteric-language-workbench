use v5.42;
package Base;
sub hi { return "base" }
package Derived;
our @ISA = ("Base");
my $o = bless {}, "Derived";
print $o->SUPER::hi(), "\n";
