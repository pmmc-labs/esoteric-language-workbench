use v5.42;
# G1: when an odd count for %opts stops the program. perl: as the sub is
# entered, before any default runs. A %opts filled "at its turn", as
# @rest is, would print `default` first.
sub t() { say "default"; return 1 }
sub f($x //= t(), %o) { return 1 }
say "before";
f(undef, "k");
