# kind: refused
# perl reads `*3` as a typeglob, warns that it isn't a number, and prints 0.
use v5.42;
say 2 * *3;
