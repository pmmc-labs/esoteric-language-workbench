# kind: refused
# perl warns `Unrecognized escape \q passed through`, and prints aqb (T86).
use v5.42;
say "a\qb";
