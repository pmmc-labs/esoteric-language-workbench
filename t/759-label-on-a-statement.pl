# kind: refused
# perl takes a label on any statement, and it does nothing there (T121).
use v5.42;
L: say 1;
