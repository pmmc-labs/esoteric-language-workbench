use v5.42;
package A; sub hi {"a"} package B; sub hi {"b"} package main; my $o = bless {}, "A"; my $x = $o->hi; bless $o, "B"; print $x, $o->hi, "\n";
