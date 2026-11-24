# kind: refused
# perl prints `(`, and warns `say (...) interpreted as function`: it looks for the
# closing bracket in the text of the line, and counts the one in the string (T100).
use v5.42;
say ("(");
