# kind: refused
# perl prints xy: the brackets are not the whole list (T320).
use v5.42;
say STDERR ("x"), "y";
