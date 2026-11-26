use v5.42;
use feature 'class', 'isa';
no warnings 'experimental::class';
class Foo {
    field $x = 1;
    ADJUST { $x = 2 }
    method m { $x }
    method idle { }
}
package Bar;
sub hi { return "bar" }
sub TIESCALAR { return bless {}, "Bar" }
sub FETCH { return "fetched" }
package Baz;
our @ISA = ("Bar");
sub hi { my $s = shift; return "baz+" . $s->SUPER::hi }
package main;
my $c = Foo->new;
my $b = bless {}, "Bar";
my $name = "hi";
my $yes = $b isa Bar;
my $code = $b->can("hi")->($b);
tie my $t, "Bar", "arg";
my $is = tied($t) ? "y" : "n";
print ref($c), $c->m, ref($b), $b->hi, $b->$name, $yes, $code, $t, $is, "\n";
my $z = bless { k => 1 }, "Baz";
print $z->hi, $z->{k}, "\n";
