# kind: refused
# perl runs it ('\n') and warns: Use of uninitialized value in say.
use v5.42;
say 5->[0];
