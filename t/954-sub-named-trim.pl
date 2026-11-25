# kind: refused
# perl warns as it compiles: Subroutine trim redefined (T28).
use v5.42;
sub trim($s) { return "mine"; }
say trim(" a ");
