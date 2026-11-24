# kind: refused
# perl prints 15: a leading zero makes a literal octal. The language writes
# octal 0o17, and a leading zero is refused (D38, T24).
use v5.42;
say 017;
