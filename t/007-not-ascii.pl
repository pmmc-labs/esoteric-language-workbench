# kind: refused
# A character past ASCII is refused wherever it stands, a comment included
# (D16), as perl 5.42 refuses it without `use utf8` (T73). Step 3.
use v5.42;
say 42; # café
