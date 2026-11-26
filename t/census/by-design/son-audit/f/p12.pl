use v5.42;
package C; our $o; sub new { bless {}, shift } sub repl { $_[0] = "g" } package main; $C::o=C->new; $C::o->repl; print ref($C::o) ? "obj" : $C::o, "\n";
