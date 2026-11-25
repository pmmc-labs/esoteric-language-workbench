# kind: refused
# perl: Can't use global $_ in subroutine signature.
use v5.42;
sub f($_) { return 1; }
