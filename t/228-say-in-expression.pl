# kind: refused
# perl prints 2 and then 2: say's value is 1. Here say is a statement.
use v5.42;
say 1 + say 2;
