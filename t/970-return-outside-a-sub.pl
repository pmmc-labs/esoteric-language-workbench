# kind: refused
# perl prints a, and dies: Can't return outside a subroutine (T139).
use v5.42;
say "a";
return;
say "b";
