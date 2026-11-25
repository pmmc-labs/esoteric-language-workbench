# kind: refused
# perl warns that `defined` without parentheses is ambiguous (T94).
use v5.42;
say defined - 1;
