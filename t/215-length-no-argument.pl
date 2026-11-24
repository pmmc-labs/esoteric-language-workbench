# kind: refused
# perl takes the length of `$_`, which the language doesn't have.
use v5.42;
say length;
