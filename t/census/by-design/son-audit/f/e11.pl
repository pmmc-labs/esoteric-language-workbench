use v5.42;
use strict; my $r="x"; my $v = eval { $$r }; print $@ ? "e":"n","\n";
