# kind: refused
# perl doesn't compile it: Can't modify constant item in preincrement.
use v5.42;
say ++5;
