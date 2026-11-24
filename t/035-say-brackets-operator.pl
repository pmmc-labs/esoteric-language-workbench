# kind: refused
# perl prints 3, and warns: the brackets are all of say's arguments, and
# the multiplication is done to what say returned and thrown away (T25).
use v5.42;
say (1 + 2) * 3;
