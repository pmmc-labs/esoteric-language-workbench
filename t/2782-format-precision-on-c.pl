# kind: refused
# perl prints nothing for %.0c.
use v5.42;
say sprintf("[%.0c]", 65);
