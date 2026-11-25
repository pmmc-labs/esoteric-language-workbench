# kind: refused
# And both branches of ? : (T104).
use v5.42;
say(1 ? ("a") x 3 : "b");
