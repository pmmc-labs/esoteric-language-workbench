# kind: refused
# perl prints x; the braces are not in the language.
use v5.42;
say {STDERR} "x";
