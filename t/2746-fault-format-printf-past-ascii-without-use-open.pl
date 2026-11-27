# kind: fault
# perl prints one byte for it, where the language would print two (D39).
use v5.42;
printf("%s\n", chr(233));
