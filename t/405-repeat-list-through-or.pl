# kind: refused
# perl repeats a list here too: the list that say's argument is reaches the right of
# `||` (T104).
use v5.42;
say(0 || ("a") x 3);
