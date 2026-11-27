# kind: fault
# perl makes the character, and warns when it is printed.
use v5.42;
say sprintf("%c", 0x110000);
