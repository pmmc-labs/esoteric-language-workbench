# kind: refused
# With exactly one blank between say and its bracket, perl looks along the
# line for the closing bracket and a semicolon, and warns `say (...)
# interpreted as function` when it doesn't find them there (T76).
use v5.42;
say (1 +
     2);
