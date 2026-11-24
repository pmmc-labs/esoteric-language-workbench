# kind: refused
# perl prints a, and joins `b` to what print returned (T25).
use v5.42;
print ("a") . "b";
